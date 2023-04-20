# import json
#
# from rest_framework import permissions
#
#
# class CustomerAccessPermission(permissions.IsAuthenticated):
#     def has_permission(self, request, view):
#         jwt_token = request.COOKIES.get('jwt')
#
#         if not jwt_token:
#             return False
#         try:
#             jwt_token = jwt_token.replace("\'", "\"")
#             jwt_dict = json.loads(jwt_token)
#
#             access_token = jwt_dict.get('access_token')
#             refresh_token = jwt_dict.get('refresh_token')
#
#             if access_token and refresh_token:
#                 return True
#             else:
#                 return False
#         except Exception as e:
#             print(f"Error parsing JWT token: {str(e)}")
#             return False
#
