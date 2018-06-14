from rest_framework.decorators import (
    api_view
)
from rest_framework.response import Response
import traceback
from .fetch_data_from_redshift import FetchDataFromRedhsift
from .generate_graph import Graphgenerator

@api_view(['POST'])
def get_user_behavior(request):

    try:
        payload = request.data
        num_users = payload.get('num_users')
        start_date = payload.get('start_date')
        end_date = payload.get('end_date')
        user_id = payload.get('user_id')

        redshift_queries = FetchDataFromRedhsift(payload)
        redshift_queries.connect_to_redshift()
        redshift_queries.query_redshift()

        graph_generator = Graphgenerator([1,2])
        graph_generator.fetch_data_from_workflow()


        return Response({"status": 200,
                         "message": 'SUCCESS'
                     }, 200)





    except Exception as e:
        print(traceback.print_exc())
        return Response({"status": 500,
                         "error":
                             {
                                 'message': 'Internal Server Error'
                             }
                         }, 500)