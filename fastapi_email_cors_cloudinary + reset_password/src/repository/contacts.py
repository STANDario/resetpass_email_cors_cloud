from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, RequestPassword
from src.database.models import User


async def get_contacts(limit: int, skip: int, user: User, db: Session):
    return db.query(Contact).filter_by(user_id=user.id).limit(limit).offset(skip).all()


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_contact_by_email(contact_email: str, user: User, db: Session):
    return db.query(Contact).filter(and_(Contact.email == contact_email, Contact.user_id == user.id)).first()


async def get_user_by_email_for_confirm(contact_email: str, db: Session):
    return db.query(User).filter(User.email == contact_email).first()


async def get_contact_by_name(contact_name: str, user: User, db: Session):
    return db.query(Contact).filter(and_(Contact.first_name == contact_name, Contact.user_id == user.id)).all()


async def get_contact_by_surname(contact_surname: str, user: User, db: Session):
    return db.query(Contact).filter(and_(Contact.surname == contact_surname, Contact.user_id == user.id)).all()


async def get_contact_by_phone(phone: str, user: User, db: Session):
    return db.query(Contact).filter(and_(Contact.phone_number == phone, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session):
    contact = Contact(**body.dict(), user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, db: Session, user: User, contact_id: int):
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_birthday_contact(user: User, db: Session):
    contacts = db.query(Contact).filter_by(user_id=user.id).all()
    contacts_result = []
    today = datetime.now().date()
    for contact in contacts:
        contact_birthday = contact.birthday.replace(year=datetime.now().year)
        maybe_seven_days = (contact_birthday - today).days
        if 0 <= maybe_seven_days <= 7:
            print(maybe_seven_days)
            contacts_result.append(contact)
    return contacts_result


async def confirmed_email(email: str, db: Session):
    user = await get_user_by_email_for_confirm(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session):
    user = await get_user_by_email_for_confirm(email, db)
    user.avatar = url
    db.commit()
    return user


async def update_password(email: str, password: RequestPassword, db: Session):
    user = await get_user_by_email_for_confirm(email, db)
    user.password = password
    db.commit()
    return user
