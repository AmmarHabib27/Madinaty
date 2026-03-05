from .authSerializers import (
    RequestOTPSerializer, VerifyOTPSerializer,
    RegisterSerializer, RegisterAndRequestOTPSerializer,
)
from .profileSerializers import ProfileSerializer, UpdateProfileSerializer
from .complaintSerializers import (
    ComplaintCreateSerializer, ComplaintListSerializer,
    ComplaintDetailSerializer, ComplaintMediaSerializer,
)
from .newsSerializers import NewsListSerializer, NewsDetailSerializer
