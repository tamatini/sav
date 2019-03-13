from sav_depot.services import api
from sav_depot import app

api.init_app(app)
app.run(debug=True)
app.register_blueprint(api.routes)
