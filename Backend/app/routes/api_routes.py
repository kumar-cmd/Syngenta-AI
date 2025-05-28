# from flask import Blueprint, jsonify, request
# from flask_security import auth_required

# api_bp = Blueprint('api', __name__)

# @api_bp.route('/query', methods=['POST'])
# # @auth_required('token')
# def query():
#     data = request.get_data(as_text=True)
#     query_text = ""
#     return jsonify({
#             'answer': f"You asked: '{query_text}' '{data}'. This is a JSON response.",
#             'type': 'text'
#         })


from flask import Blueprint, request, jsonify
from app.utils.query_classifier import queryClassifier
from app.utils.llama_index import query_documents

from flask_cors import cross_origin

api_bp = Blueprint('api', __name__)


@api_bp.route('/query', methods=['POST', 'OPTIONS'])
@cross_origin(origins="https://syngent-ai.vercel.app", allow_headers=["Content-Type"])
def query():
    if request.content_type == 'application/json':
        data = request.get_json()
        query_text = data.get('query', '')
        context = data.get('context', {})

        query_type = queryClassifier(query_text)

        if query_type == 'document':
            result = query_documents(query_text)
            return jsonify({
                'answer': result["answer"],
                'sources': result["sources"],
                'type': 'document'
            })

        return jsonify({'error': 'Unrecognized query type'}), 400

    return jsonify({'error': 'Unsupported Content-Type'}), 415


# @api_bp.route('/query', methods=['POST', 'OPTIONS'])
# @cross_origin(origins="https://syngent-ai.vercel.app", allow_headers=["Content-Type"])
# def query():
#     # For JSON requests
#     if request.content_type == 'application/json':
#         data = request.get_json()
#         query_text = data.get('query', '')
#         context = data.get('context', {})

#         query_type = queryClassifier(query_text)

#         if query_type == 'document':
#             result = query_documents(query_text)
#         # elif query_type == 'sql':
#         #     answer = handle_sql_query(user_query)
#         # else:
#         #     answer = "Could not classify query."
#         # return jsonify({'answer': answer})

#         return jsonify({
#             'answer': f'You asked: "{query_text}". This is a JSON response : {result}.',
#             'type': 'text'
#         })

#     # # For multipart form-data (e.g., file uploads + form fields)
#     # elif request.content_type.startswith('multipart/form-data'):
#     #     query_text = request.form.get('query', '')
#     #     file = request.files.get('file')  # Optional file input

#     #     print(f"[FORM] Query: {query_text}")
#     #     if file:
#     #         print(f"Received file: {file.filename}, Type: {file.mimetype}")

#     #     return jsonify({
#     #         'answer': f'Received form query: "{query_text}". File: {file.filename if file else "No file"}',
#     #         'type': 'text'
#     #     })

#     return jsonify({'error': 'Unsupported Content-Type'}), 415
