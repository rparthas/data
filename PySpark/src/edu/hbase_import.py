from starbase import Connection

c = Connection("localhost", 8000)
print("Conn created")

ratings = c.table('ratings')
print("table created")

if ratings.exists():
    ratings.drop()

ratings.create('rating')
print("CF created")


rating_file = open("../../data/HadoopMaterials/ml-100k/u.data", "r")

batch = ratings.batch()

for line in rating_file:
    try:
        (user_id, movie_id, rating, timestamp) = line.split("\t")
        batch.update(user_id, {movie_id: rating})
    except:
        continue

print("batch created")

rating_file.close()
batch.commit(True)

print(ratings.fetch("33"))
