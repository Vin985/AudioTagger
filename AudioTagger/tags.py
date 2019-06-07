import yaml


class Tags:
    def __init__(self):
        self.next_id = 1
        self.tags = {}

    def add(self, name, color, keyseq, related=[]):
        tag_id = self.next_id
        tag = Tag(tag_id, name, color, keyseq, related)
        self.tags[tag_id] = tag
        self.next_id += 1
        return tag

    def __getitem__(self, key):
        print("getting item with key " + str(key))
        return self.tags[key]

    def __str__(self):
        res = ''
        for value in self.tags.values():
            res += str(value) + "\n"
        return res

    def save(self, path):
        stream = open(path, 'w')
        yaml.dump(self.tags, stream)

    def load(self, path=""):
        try:
            stream = open(path, 'r')
            self.tags = yaml.load(stream, Loader=yaml.Loader) or {}
            self.check_dependencies()
            # ids = [tag.id for tag in self.tags]
            if self.tags:
                self.next_id = max(self.tags.keys()) + 1
        except FileNotFoundError:
            print("file not found")

    def check_dependencies(self):
        # here check that all related tags actually exist
        pass

    def get_key_sequences(self):
        return [tag.keyseq for tag in self.tags.values()]

    def get_names(self):
        return [tag.name for tag in self.tags.values()]

    def get_color(self, name):
        for tag in self.tags.values():
            if tag.name == name:
                return tag.name
        return None

    def remove_empty(self):
        res = {key: value for key, value in self.tags.items() if value.name}
        print("in remove empty")
        print(res)
        self.tags = res
        self.next_id = max(self.tags.keys()) + 1


class Tag:
    def __init__(self, id, name, color, keyseq, related=None):
        self.id = id
        self.name = name
        self.color = color
        self.keyseq = keyseq
        self.related = []
        if related:
            if not isinstance(related, list):
                self.related.append(related)
            else:
                self.related = related

    def add_parent(self, parent):
        print("adding parent {} for tag {}".format(parent, self.name))
        if not isinstance(parent, list):
            self.related.append(parent)
        else:
            self.related += parent

    def get_tags(self):
        res = []
        print(self.name)
        res.append(self.name)
        for tag in self.related:
            res.append(tag.get_tags())
        return res

    def __str__(self):
        return("Tag object with id: {0}, name: {1}. Related tags: {2}".format(str(self.id),
                                                                              str(self.name),
                                                                              str(self.related)))


# tags = Tags()
# t1 = tags.add("test")
# t2 = tags.add("test2", [t1])
# t3 = tags.add("test3")
# print(len(t1.related))
# t3.add_parent(t2)
# print(len(t1.related))
# print(tags)
# tags.save("test.yaml")
# tags2 = Tags()
# tags2.load("test.yaml")
# print(tags)
# print(tags2)
# # t2.get_tags()
# # t3.get_tags()
#
# print(tags[1])
