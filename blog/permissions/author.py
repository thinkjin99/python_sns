from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    # 인증된 유저에 한해, 목록조회/포스팅등록 허용
    def has_permission(self, request, view):
        return request.user.is_authenticated

    # 작성자에 한해 레코드에 대한 수정/삭제 허용
    def has_object_permission(self, request, view, obj):
        # 조회 요청(GET, HEAD, OPTIONS) 에 대해 인증여부 상관없이 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author == request.user

        # PUT, DELETE 요청에 대해 작성자일 경우 요청 허용


class OnlyAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
