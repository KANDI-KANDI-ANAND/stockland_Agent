from backend.app.database.models.interest import Interest


class InterestRepository:

    @staticmethod
    async def create_interest(db, data):

        interest = Interest(
            name=data.get("name"),
            phone=data.get("phone"),
            email=data.get("email"),
            community=data.get("community"),
            message=data.get("message")
        )

        db.add(interest)

        await db.commit()

        await db.refresh(interest)

        return interest