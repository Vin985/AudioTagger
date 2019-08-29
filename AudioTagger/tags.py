import yaml


class Tags:
    def __init__(self):
        self.tags = {}

    def add(self, name, color=None, keyseq=None, related=[]):
        tag = Tag(name, color, keyseq, related)
        self.tags[name] = tag
        return tag

    def delete(self, name):
        del self.tags[name]

    def update_name(self, old, new):
        tag = self.tags[old]
        tag.name = new
        self.tags[new] = tag
        del self.tags[old]

    def __getitem__(self, key):
        # print("getting item with key " + str(key))
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
            tmp = yaml.load(stream, Loader=yaml.Loader) or {}
            for v in tmp.values():
                self.tags[v.name] = v
            self.check_dependencies()
            # ids = [tag.id for tag in self.tags]
            # if self.tags:
            #     self.next_id = max(self.tags.keys()) + 1
        except FileNotFoundError:
            print("file not found")

    def check_dependencies(self):
        # here check that all related tags actually exist
        pass

    def get_key_sequences(self):
        return [tag.keyseq for tag in self.tags.values()]

    def get_names(self):
        return list(self.tags.keys())
        # return [tag.name for tag in self.tags.values()]

    def get_color(self, name):
        return self.tags[name].color
        # for tag in self.tags.values():
        #     if tag.name == name:
        #         return tag.color
        # return None

    def remove_empty(self):
        res = {key: value for key, value in self.tags.items(
        ) if value.name and value.name != "<New Tag>"}
        self.tags = res
        # self.next_id = max(self.tags.keys()) + 1


class Tag:
    def __init__(self, name, color, keyseq, related=None):
        self.name = name
        self.color = color
        self.keyseq = keyseq
        self.related = []
        if related:
            if not isinstance(related, list):
                self.related.append(related)
            else:
                self.related = related

    def add_related(self, tags):
        print("adding parent {} for tag {}".format(tags, self.name))
        if not isinstance(tags, list):
            self.related.append(tags)
        else:
            self.related += tags

    def remove_related(self, tag):
        self.related.remove(tag)

    # def get_related(self, root=True):
    #     print(self.name)
    #     res = []
    #     if not root:
    #         res.append(self.id)
    #     for tag in self.related:
    #         res += tag.get_related(root=False)
    #     return res

    def get_related(self, level=0, as_list=True, min_level=-1, max_level=-1):
        res = set()
        if level > 0 and level > min_level:
            res.add(self.name)
        if max_level > 0 and level == max_level:
            return res
        for tag in self.related:
            res.update(tag.get_related(level=level + 1,
                                       min_level=min_level, max_level=max_level))
        if level == 0 and as_list:
            return list(res)
        return res

    def get_related_ids(self):
        res = []
        res.append(self.name)

    def __str__(self):
        return("Tag object with name: {0}. Related tags: {1}".format(str(self.name),
                                                                     str(self.related)))


# tags = Tags()
# t1 = tags.add("test")
# t2 = tags.add("test2", related=[t1])
# t3 = tags.add("test3")
# t32 = tags.add("test32")
# t4 = tags.add("test4", related=[t32, t2])
# t3.add_related(t2)
# print(tags)
# # tags.save("test.yaml")
# # tags2 = Tags()
# # tags2.load("test.yaml")
# # print(tags)
# # print(tags2)
# print(t2.get_related())
# print(t3.get_related(max_level=1))
# print(t4.get_related(min_level=1))
# # t3.get_related()
