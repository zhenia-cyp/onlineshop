from goods.models import Product
from django.contrib.postgres.search import (
    SearchVector,
    SearchRank,
    SearchHeadline,
    SearchQuery,
)



def q_search(query):
    """Search by product ID"""
    if query.isdigit() and len(query) <= 5:
        return Product.objects.filter(id=int(query))

    words = query.split()
    vector = SearchVector("name", "description")

    query_list = [SearchQuery(word) for word in words]

    if len(query_list) > 1:
        combined_query = query_list[0]
        for q in query_list[1:]:
            combined_query = combined_query |  q
        
    else:
        combined_query = query_list[0]

    result = (
        Product.objects.annotate(rank=SearchRank(vector, combined_query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            combined_query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            combined_query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    return result

  
