from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, String, Integer, Float, ForeignKey, Table, Column
from datetime import date

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


compare_counties = Table(
    'compare_counties',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('fips_id', String, ForeignKey('county_data.fips_id'))
)

# class Compare_county(Base):
#     __tablename__ = 'compare_counties'

#     user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
#     fips_id: Mapped[str] = mapped_column(String(360), ForeignKey('county_name_mapping.fips_id'))

#     user: Mapped['User'] = relationship('User', back_populates='compare_counties')
#     county_name_mapping: Mapped['County_name_mapping'] = relationship('County_name_mapping', back_populates='compare_counties')
#     county_data: Mapped['County_data'] = relationship('County_data', back_populates='compare_counties')


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key = True)
    first_name: Mapped[str] = mapped_column(String(360), nullable=False)
    last_name: Mapped[str] = mapped_column(String(360), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    role: Mapped[str] = mapped_column(String(360), nullable=False, default="free_user")

    county_data: Mapped[list['County_data']] = relationship('County_data', secondary='compare_counties', back_populates='users')


class County_data(Base):
    __tablename__ = 'county_data'
    
    fips_id: Mapped[str] = mapped_column(String(360), ForeignKey('county_name_mapping.fips_id'), primary_key = True, nullable=False)
    info_date: Mapped[date] = mapped_column(Date, primary_key = True, nullable=False)
    median_listing_price: Mapped[float] = mapped_column(nullable=False)
    active_listing_count: Mapped[int] = mapped_column(nullable=False)
    active_listing_count_yy: Mapped[float] = mapped_column(nullable=False)
    median_days_on_market: Mapped[int] = mapped_column(nullable=False)
    price_reduced_count: Mapped[int] = mapped_column(nullable=False)
    # pending_listing_count: Mapped[int] = mapped_column(nullable=False)?

    users: Mapped[list['Users']] = relationship('Users', secondary='compare_counties', back_populates='county_data')
    county_name_mapping: Mapped['County_name_mapping'] = relationship('County_name_mapping', back_populates='counties_data')


# changing county name to separate table to quickly handle county name changes
class County_name_mapping(Base):
    __tablename__ = 'county_name_mapping'

    fips_id: Mapped[str] = mapped_column(String(360), primary_key=True, nullable=False)
    county_name: Mapped[str] = mapped_column(String(360), nullable=False)

    counties_data: Mapped[list['County_data']] = relationship('County_data', back_populates='county_name_mapping')
    
