from .database import Base, engine
from .models import AccidentEvent

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized and tables created.")
