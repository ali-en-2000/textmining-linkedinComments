
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment, Post, miningData
from .serializers import PostSerializer
from django.http import JsonResponse
from .linkedin_scraper import scrape_linkedin_comments

from .mining import mining_comments



class addPostView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            post = serializer.save()
            names, comments = scrape_linkedin_comments(request.data['url'], request.data['email'], request.data['password'])
            for i in range(len(comments)):
                new_comment = Comment(
                    postUrl=request.data['url'],
                    author=names[i],
                    text=comments[i]
                )
                new_comment.save()
            
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCommmentsView(APIView):
    def get(self, request):
        url = request.GET.get('url', None)
        if url is not None:
            comments = Comment.objects.filter(postUrl__icontains=url)
            comments_list = []
            for comment in comments:
                comment_dict = {'id': comment.id,
                                'author': comment.author, 'comment': comment.text}
                comments_list.append(comment_dict)
            return Response({'comments': comments_list}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'no URL parameter provided'}, status=status.HTTP_400_BAD_REQUEST)

class GetCommmentsMindedView(APIView):
    def get(self, request):
        url = request.GET.get('url', None)
        if url is not None:
            comments = miningData.objects.filter(postUrl__icontains=url)
            comments_list = []
            for comment in comments:
                print(comment)
                comment_dict = {'id': comment.id,
                                'author': comment.author,
                                'comment': comment.text,
                                'veder_neg': comment.vader_neg,
                                'vader_neu': comment.vader_neu,
                                'vader_pos': comment.vader_pos,
                                'vader_compound': comment.vader_compound,
                                'roberta_neg': comment.roberta_neg,
                                'roberta_neu': comment.roberta_neu,
                                'roberta_pos': comment.roberta_pos                  
                                }
                comments_list.append(comment_dict)
            return Response({'comments': comments_list}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'no URL parameter provided'}, status=status.HTTP_400_BAD_REQUEST)


class GetCommmentsDataminedView(APIView):
    def get(self, request):
        url = request.GET.get('url', None)
        mining_comments(url)

        if url is not None:

            comments = miningData.objects.filter(postUrl__icontains=url)
            comments_list = []
            for comment in comments:
                comment_dict = {'id': comment.id,
                                'author': comment.author, 'comment': comment.text,
                                'vader_neg': comment.vader_neg, 'vader_neu': comment.vader_neu, 'vader_pos': comment.vader_pos,'vader_compound': comment.vader_compound,
                                'roberta_neg': comment.roberta_neg, 'roberta_neu': comment.roberta_neu,'roberta_pos': comment.roberta_pos, }
                comments_list.append(comment_dict)
            return Response({'comments': comments_list}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'no URL parameter provided'}, status=status.HTTP_400_BAD_REQUEST)


class deleteCommmentsView(APIView):
    def get(self, request):
        url = request.GET.get('url', None)
        if url is not None:
            comments = Comment.objects.filter(postUrl__icontains=url)
            comments.delete()
            minningData = miningData.objects.filter(postUrl__icontains=url)
            minningData.delete()
            post = Post.objects.filter(url__icontains=url)
            post.delete()
        return Response({'status': 'deleted'})


def post_list(request):
    posts = Post.objects.all().values('url', 'email', 'password')
    data = {'posts': list(posts)}
    return JsonResponse(data)
