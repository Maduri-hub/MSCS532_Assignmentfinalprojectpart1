import heapq
import time

# Global cache for similarity computations
similarity_cache = {}

class UserProductGraph:
    def __init__(self):
        self.graph = {}  # Dictionary mapping users to sets of products

    def add_user(self, user_id):
        if user_id not in self.graph:
            self.graph[user_id] = set()

    def add_product(self, user_id, product_id):
        if user_id in self.graph:
            self.graph[user_id].add(product_id)
        else:
            self.graph[user_id] = {product_id}

    def get_products(self, user_id):
        return self.graph.get(user_id, set())

    def get_users(self):
        return list(self.graph.keys())

class RecommendationHeap:
    def __init__(self, n=5):
        self.heap = []
        self.max_size = n

    def add_recommendation(self, score, product_id):
        heapq.heappush(self.heap, (-score, product_id))

    def get_top_recommendations(self):
        return [heapq.heappop(self.heap)[1] for _ in range(min(self.max_size, len(self.heap)))]
        
def calculate_similarity(user1, user2, user_graph):
    key = tuple(sorted((user1, user2)))  # Ensure uniqueness
    if key in similarity_cache:
        return similarity_cache[key]

    products1 = user_graph.get_products(user1)
    products2 = user_graph.get_products(user2)
    sim = len(products1.intersection(products2))

    similarity_cache[key] = sim
    return sim

def recommend_for_user(user_id, user_graph):
    user_products = user_graph.get_products(user_id)
    recommendations = {}

    for other_user in user_graph.get_users():
        if other_user == user_id:
            continue
        
        sim = calculate_similarity(user_id, other_user, user_graph)
        if sim > 0:
            other_products = user_graph.get_products(other_user)
            for product in other_products - user_products:
                recommendations[product] = recommendations.get(product, 0) + sim

    rec_heap = RecommendationHeap(n=5)
    for product, score in recommendations.items():
        rec_heap.add_recommendation(score, product)

    return rec_heap.get_top_recommendations()

# Test the implementation
def run_tests():
    user_graph = UserProductGraph()
    
    # Adding users and products
    user_graph.add_user("user1")
    user_graph.add_product("user1", "productA")
    user_graph.add_product("user1", "productB")
    
    user_graph.add_user("user2")
    user_graph.add_product("user2", "productB")
    user_graph.add_product("user2", "productC")
    
    user_graph.add_user("user3")
    user_graph.add_product("user3", "productA")
    user_graph.add_product("user3", "productD")
    
    print("User1 Products:", user_graph.get_products("user1"))
    print("User2 Products:", user_graph.get_products("user2"))
    print("User3 Products:", user_graph.get_products("user3"))
    
    # Recommendations
    recommendations = recommend_for_user("user1", user_graph)
    print("Top Recommendations for user1:", recommendations)

if __name__ == "__main__":
    run_tests()
