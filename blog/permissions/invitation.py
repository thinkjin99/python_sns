from permissions.author import OnlyAuthor


class InvitationPermission(OnlyAuthor):
    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj): #초대 발급자는 수락/거절 설정 불가
            if request.method in ["PUT", "PATCH"]:
                # 수락/거절 상태 변경 불가
                return "status" not in request.data
            return True

        # 글 작성자는 수락/거절 상태만 변경 가능
        elif obj.post.author == request.user:
            if request.method in ["PUT", "PATCH"]:
                return set(request.data.keys()) <= {"status"} #변경사항에 status만 존재하는지 확인 (부분집합)
