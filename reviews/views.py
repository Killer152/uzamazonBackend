from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from PIL import Image
from reviews.models import ReviewModel
from reviews.serializers import ReviewCreateSerializer, ReviewListSerializer
from shop.models import ProductModel
from shop.utils import paginate


class ReviewCreateView(CreateAPIView):
    """Creates review
    POST:
    {
        stars: int,
        comment: str,
    }
    additional: image_1, image_2, image_3, image_4 -> img

    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewCreateSerializer

    def create(self, request, *args, **kwargs):
        product = get_object_or_404(ProductModel, slug=self.kwargs.get('product'))
        i1 = self.request.FILES.get('image_1')
        i2 = self.request.FILES.get('image_2')
        i3 = self.request.FILES.get('image_3')
        i4 = self.request.FILES.get('image_4')
        a = [i1, i2, i3, i4]
        n = 0
        for i in a:
            n += 1
            if i is not None:
                try:
                    trial_image = Image.open(i)
                    trial_image.load()
                    if hasattr(i, 'reset'):
                        i.reset()
                    trial_image = Image.open(i)
                    trial_image.verify()
                except Exception:
                    return Response({"message": "Invalid image"}, status=status.HTTP_400_BAD_REQUEST)
            if n == 1:
                img1 = i
            elif n == 2:
                img2 = i
            elif n == 3:
                img3 = i
            elif n == 4:
                img4 = i
        ReviewModel.objects.create(user=self.request.user, product=product, image_1=img1, image_2=img2, image_3=img3,
                                   image_4=img4, stars=self.request.data['stars'], comment=self.request.data['comment'])
        product.star_count += 1
        product.star_total += int(self.request.data['stars'])
        product.save()
        return Response({"message": "Review has been created"}, status=status.HTTP_201_CREATED)


class ReviewListView(ListAPIView):
    """List of product`s reviews"""
    serializer_class = ReviewListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        return ReviewModel.objects.filter(product__slug=self.kwargs['product'])

    def get(self, request, *args, **kwargs):
        return paginate(request, self.get_queryset(), self.get_serializer)


class ReviewDetailView(RetrieveAPIView):
    """Detail info about review"""
    def get(self, request, *args, **kwargs):
        count = ReviewModel.objects.filter(product__slug=self.kwargs['product']).count()
        reviews = ReviewModel.objects.filter(product__slug=self.kwargs['product'])
        try:
            star_1 = reviews.filter(stars=1).count() / count * 100
            star_2 = reviews.filter(stars=2).count() / count * 100
            star_3 = reviews.filter(stars=3).count() / count * 100
            star_4 = reviews.filter(stars=4).count() / count * 100
            star_5 = reviews.filter(stars=5).count() / count * 100
        except ZeroDivisionError:
            star_1 = 0
            star_2 = 0
            star_3 = 0
            star_4 = 0
            star_5 = 0

        data = {
            'rate': get_object_or_404(ProductModel, slug=self.kwargs['product']).rate,
            'count': count,
            'star_1': int(star_1),
            'star_2': int(star_2),
            'star_3': int(star_3),
            'star_4': int(star_4),
            'star_5': int(star_5),
        }
        return Response(data=data, status=status.HTTP_200_OK)
