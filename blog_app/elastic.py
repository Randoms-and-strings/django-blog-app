from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

if client.indices.exists(index="blog_posts") is False:
    client.indices.create(index="blog_posts")