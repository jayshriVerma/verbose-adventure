from flask import Flask
from flask_restful import Api,Resource,reqparse,abort,fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name = {name},views = {views}, likes = {likes})" 


db.create_all()
		
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required",required=True)
video_put_args.add_argument("views", type=int, help="views of the video is required",required=True)
video_put_args.add_argument("likes", type=int, help="likes of the video is required",required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="views of the video is required")
video_update_args.add_argument("likes", type=int, help="likes of the video is required")

'''video_delete_args = reqparse.RequestParser()
video_delete_args.add_argument("name", type=str, help="Name of the video is required")
video_delete_args.add_argument("views", type=int, help="views of the video is required")
video_delete_args.add_argument("likes", type=int, help="likes of the video is required")'''


#videos = {}

#def abort_if_video_doesnt_exist(video_id):
#	if video_id not in videos:
#		abort(404,message="video id is not valid....")

#def abort_if_video_exist(video_id):
#	if video_id in videos:
#		abort(409,message="video id already exist....")

resource_fields = {
		'id' : fields.Integer,
		'name':fields.String,
		'views':fields.Integer,
		'likes':fields.Integer
}	

class Video(Resource):
	@marshal_with(resource_fields)
	def get(self,video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Couldn't find video with that id")
		return result


	@marshal_with(resource_fields)
	def put(self,video_id):
		#abort_if_video_exist(video_id)
		args = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if result:
			abort(409,message="Video id already exist.choose other one....")
		video = VideoModel(id=video_id,name=args['name'],views=args['views'],likes=args['likes'])
		#videos[video_id] = args
		db.session.add(video)
		db.session.commit()
		return video, 201

	@marshal_with(resource_fields)
	def patch(self,video_id):
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="video doesn't exist,cann't update.")

		if args['name']:
			result.name = args['name']
		if args['views']:
		    result.views =args['views']
		if args['likes']:
		   	result.likes = args['likes']

		db.session.commit()  
		
		return result	
		
	@marshal_with(resource_fields)	
	def delete(self,video_id):
		# abort_if_video_doesnt_exist(video_id)
		# del videos[video_id]
		# return '',204
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="video doesn't exist.")
	

		'''if args['name']:
			result.name = args['name']
		if args['views']:
		    result.views =args['views']
		if args['likes']:
		   	result.likes = args['likes']'''

		db.session.delete(result)
		db.session.commit()  
		
		return result	


api.add_resource(Video,"/video/<int:video_id>")	


if __name__ == "__main__":
	app.run(debug=True)