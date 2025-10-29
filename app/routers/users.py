from fastapi import APIRouter, Depends
from app.schemas.user import UserRead, UserCreate
from app.db.session import get_db
from sqlalchemy.orm import session
from app.repository.users import UserRepository
from app.schemas.token import TokenData
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.auth.email_utils import send_otp_email
from fastapi import BackgroundTasks

user_router = APIRouter(prefix="/users")

@user_router.post(
    path="/register",
    response_model= UserRead,
    description="User Registration")
async def user_register( user_create: UserCreate, background_tasks:BackgroundTasks, Session: session = Depends(get_db)):
    user_repo = UserRepository(db=Session)
    new_user = user_repo.user_register_repo(user_create)
    await send_otp_email(background_tasks, new_user.email, new_user.otp_code)
    return new_user

@user_router.post(
    path="/verify-email",
    description="User Verification"
)
def verify_user(email: str, otp: str, Session: session = Depends(get_db)):
    user_repo = UserRepository(db= Session)
    return user_repo.verify_user_repo(email= email, otp=otp)

@user_router.post(
    path = "/login",
    description="login page"
    )   
def user_login(request: OAuth2PasswordRequestForm = Depends(), Session = Depends(get_db)):
    print(f"inside router")
    user_repo = UserRepository(db = Session)
    access_token =  user_repo.login_user_repo(email=request.username,password=request.password)
    print(f"access_token:{access_token}")
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.post(
    path="/sendmail"   
)
async def send_mail(background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject="Testing FastAPI Mail",
        recipients= ["srinivasreddy191197@gmail.com"],
        body="Hello",
        subtype="plain" 
    )
    conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs
)
    fm = FastMail(config=conf)
    background_tasks.add_task(fm.send_message, message)
    return {"message": "Email sent successfully!"}

    





    