import db

db.start(3)

d = db.Db()
d.add("foo")
d.add_vec(["apple","baz"])
for s in ["apple","pear","foo","baz","bar"]:
    print("%7s -> %s" % (s,d.contains(s)))

db.stop()
