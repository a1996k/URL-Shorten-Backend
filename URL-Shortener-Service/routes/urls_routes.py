from fastapi import APIRouter, Depends, Request
from config.database import SessionLocal,get_db
from models.url import Url
from models.user import User
from datetime import date as Date
from datetime import date, timedelta
import services.url_service as url_services
from services.user_service import get_current_user
from starlette.responses import JSONResponse
from fastapi.responses import RedirectResponse
url = APIRouter()

@url.get("/history_urls")
async def read_all_urls(request: Request,db: SessionLocal = Depends(get_db)):
    try:
        data = await request.json()
        email = data.get("user_email")
        history = []
        urls = urls = db.query(Url).filter(Url.user_email == email)
        for url in urls:
            history.append({"short_url": url.shorturl, "longurl": url.longurl, "user_email": url.user_email, "createdDate": str(url.createdDate), "expiryDate": str(url.expiryDate)})
        print(history)
        response = JSONResponse({"history": history})
        response.status_code = 200
        return response
    except Exception as err:
        response = JSONResponse({"msg": str(err)})
        response.status_code = 400
        return response


@url.post("/url_shortner")
async def url_shortner(request: Request, db: SessionLocal = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        print(current_user)
        data = await request.json()
        longurl = data.get("longurl")
        custom_short_url = data.get("custom_short_url")
        if custom_short_url:
            short_url = custom_short_url
            shorturl_exists = db.query(Url).filter(Url.shorturl == short_url).scalar()
            if shorturl_exists:
                return {"message" : "shorturl already exists"}
        else:
            short_url = url_services.long_to_short(url=longurl)
        longurl_exists = db.query(Url).filter(Url.longurl == longurl).scalar()
        if not longurl_exists:
            user = db.query(User).filter(User.email == current_user).first()
            no_of_requests = user.no_of_requests
            if (user.tier == 1 and user.no_of_requests <1000) or (user.tier == 2 and user.no_of_requests <100):
                shorturl_exists = db.query(Url).filter(Url.shorturl == short_url).scalar()
                if not shorturl_exists:
                    url = Url(shorturl=short_url, longurl=longurl, user_email = current_user ,createdDate=date.today(), expiryDate=date.today() + timedelta(days=30))
                    db.add(url)
                    db.commit()
                    no_of_requests += 1
                    db.query(User).filter(User.email == current_user).update({'no_of_requests':no_of_requests})
                    db.commit()
                    response = JSONResponse({"short_url": str(short_url)})
                    response.status_code = 201
                    return response
                else:
                    await url_shortner(longurl, db=db)
            else:
                return {'message' : 'no of requests exceded'}
        else:
            shorturl = db.query(Url).filter(Url.longurl == longurl).first() 
            short_url = shorturl.shorturl
            response = JSONResponse({"short_url": str(short_url)})
            response.status_code = 201
            return response
    except Exception as err:
        response = JSONResponse({"message": str(err)})
        response.status_code = 400
        return response
    
@url.get("/url/{short_url}")
async def redirect(short_url: str, db: SessionLocal = Depends(get_db)):
    print(short_url)
    url = db.query(Url).filter(Url.shorturl == short_url).first()
    longurl = url.longurl
    return RedirectResponse(longurl)