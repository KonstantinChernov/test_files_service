from sqlalchemy.dialects.postgresql import UUID

from db.pg_db import db


class File(db.Model):
    __tablename__ = 'file'

    filename = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    path = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='SET NULL')
    )

    def __str__(self):
        return f'<File {self.filename}>'
