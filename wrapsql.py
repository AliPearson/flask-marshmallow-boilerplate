from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
import json
import datetime
import time
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import ValidationError, Schema, fields, validate
from flask import Response

# Initialize DB and define columns
class Base(DeclarativeBase):
	pass

class Computation(Base):
	__tablename__ = "computations"
	id: Mapped[int] = mapped_column(primary_key=True)
	calculation_type: Mapped[str] = mapped_column(String(30))
	x_value: Mapped[float] = mapped_column()
	y_translation: Mapped[int] = mapped_column()
	started_at: Mapped[str] = mapped_column()
	finished_seconds: Mapped[int] = mapped_column(nullable=True)
	result: Mapped[Optional[str]] = mapped_column(nullable=True)
	error: Mapped[Optional[str]] = mapped_column(nullable=True)
	def __repr__(self) -> str:
		return f"Computation(id={self.id!r}, calculation_type={self.calculation_type}, x_value={self.x_value!r}, y_translation={self.y_translation!r}, started_at={self.started_at!r}, result={self.result!r}, error={self.error!r})"
	def __json__(self) -> str:
		result_dict = {}
		result_dict['id'] = self.id
		result_dict['calculation_type'] = self.calculation_type
		result_dict['x_value'] = self.x_value
		result_dict['y_translation'] = self.y_translation
		result_dict['started_at'] = self.started_at
		if self.result is None:
			result_dict['result'] = None
		else:
			result_dict['result'] = json.loads(self.result)
		if self.error is None:
			result_dict['error'] = None
		else:
			result_dict['error'] = json.loads(self.error)
		return json.dumps(result_dict, indent=4)

# Create engine and database on disc
engine = create_engine("sqlite:///computations.db", echo=True)
Computation.__table__.drop(engine)
Base.metadata.create_all(engine)

# # Define Computation schema that can be dumped by marshmallow and therefore no need for __json__ function...
class ComputationSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Computation
		include_fk = True
		load_instance = True

# Define an input class 
class Post:
	def __init__(self, calculation_type, x_value, y_translation):#, started_at):
		self.calculation_type = calculation_type
		self.x_value = x_value
		self.y_translation = y_translation
		#self.started_at = started_at

class PostSchema(Schema):
	calculation_type = fields.Str(validate=validate.OneOf(["red", "green", "blue"]))
	x_value = fields.Float()
	y_translation = fields.Int(validate=validate.Range(min=-10, max=10, min_inclusive=True, max_inclusive=True))
	#started_at = fields.DateTime()

def add_row(params):
	"""
	Add a new row to the table
	"""
	session = Session(engine)
	post_schema = PostSchema()
	data=post_schema.load(params)
	nrows = session.query(Computation).count()
	id = nrows + 1
	newrow = Computation(
		id=id,
		calculation_type=data['calculation_type'],
		x_value=data['x_value'],
		y_translation=data['y_translation'],
		started_at=str(datetime.datetime.now()),
		finished_seconds=None,
		result=None,
		error=None
	)
	session.add_all([newrow])
	session.commit()
	return id

def show_table(since=None):
	"""
	Grab the entire table
	"""
	session = Session(engine)
	comp_schema = ComputationSchema(only = ["calculation_type", "x_value", "y_translation", "started_at", "result", "error"])
	if not since:  # If no since parameter
		data = []
		#session = Session(engine)
		for x in session.scalars(select(Computation)):
			data.append(json.loads(x.__json__()))
			#data.append(comp_schema.dump(x))
		return json.dumps(data, indent=4)
	else:
		since = int(since)
		data = []
		#session = Session(engine)
		for x in session.scalars(select(Computation)):
			if x.finished_seconds is None:
				pass
			else:
				if int(time.time()) - x.finished_seconds <= since:
					data.append(json.loads(x.__json__()))
					#data.append(comp_schema.dump(x))
		return json.dumps(data, indent=4)

def on_complete(id, result):
	session = Session(engine)
	stmt = select(Computation).where(Computation.id == id)  # grab the id
	computaysh = session.scalars(stmt).one()
	result_time = str(datetime.datetime.now())
	result_dict={"completed_at": result_time, "result": result}
	computaysh.result = json.dumps(result_dict)
	computaysh.finished_seconds = int(time.time())
	session.commit()

def on_error(id, message):
	session = Session(engine)
	stmt = select(Computation).where(Computation.id == id)
	computaysh = session.scalars(stmt).one()
	error_time = str(datetime.datetime.now())
	error_dict = {"errored_at": error_time, "message": message}
	computaysh.error = json.dumps(error_dict)
	computaysh.finished_seconds = int(time.time())
	session.commit()

def get_id(id):
	session = Session(engine)
	row=session.scalars(select(Computation).where(Computation.id ==id))
	return row.fetchall()

