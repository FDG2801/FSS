tasks = {
    "voc": {
        "offline":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            },
        "15-5":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                1: [16, 17, 18, 19, 20]
            },
        "15-1":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                1: [16],
                2: [17],
                3: [18],
                4: [19],
                5: [20]
            },
        "5-0m":
            {
                0: [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                1: [1],
                2: [2],
                3: [3],
                4: [4],
                5: [5]
            },
        "5-0":
            {
                0: [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                1: [1, 2, 3, 4, 5]
            },
        "5-1":
            {
                0: [1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                1: [6, 7, 8, 9, 10]
            },
        "5-1m":
            {
                0: [1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                1: [6],
                2: [7],
                3: [8],
                4: [9],
                5: [10]
            },
        "5-2":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 17, 18, 19, 20],
                1: [11, 12, 13, 14, 15]
            },
        "5-2m":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 17, 18, 19, 20],
                1: [11],
                2: [12],
                3: [13],
                4: [14],
                5: [15]
            },
        "5-3":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                1: [16, 17, 18, 19, 20]
            },
        "5-3m":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                1: [16],
                2: [17],
                3: [18],
                4: [19],
                5: [20]
            },
    },
    "cts": {
        "offline":
            {
                0: [7, 8, 11, 12, 13, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33],
            },
        "bv":
            {
                0: [7, 8, 11, 12, 13, 17, 19, 20, 21, 22, 23, 24, 25, 26, 32, 33],
                1: [27, 28, 29, 30, 31]
            },
    },
    "coco": {
        "offline":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 31,
                    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
                    58, 59, 60, 61, 62, 63, 64, 65, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 87,
                    88, 89, 90],
            },
        "voc":
            {
                0: [1, 8, 10, 11, 13, 14, 15, 22, 23, 24, 25, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
                    43, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 65, 70, 73, 74, 75, 76, 77, 78,
                    79, 80, 81, 82, 84, 85, 86, 87, 88, 89, 90],  # 53589 train img
                1: [2, 3, 4, 5, 6, 7, 9, 16, 17, 18, 19, 20, 21, 44, 62, 63, 64, 67, 72]  # voc classes w/out person
            },
        "7ss":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 27, 28, 31, 32, 35,
                    36, 37, 38, 39, 40, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63,
                    64, 65, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 88, 89, 90],
                1: [21, 25, 33, 34, 41, 57, 87]
            },
        "7mc":
            {
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 27, 28, 31, 32, 35,
                    36, 37, 38, 39, 40, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63,
                    64, 65, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 88, 89, 90],
                1: [21],
                2: [25],
                3: [33],
                4: [34],
                5: [41],
                6: [57],
                7: [87]
            },
        "20-0":
            {
                0: [2, 3, 4, 6, 7, 8, 10, 11, 13, 15, 16, 17, 19, 20, 21, 23, 24,
                    25, 28, 31, 32, 34, 35, 36, 38, 39, 40, 42, 43, 44, 47, 48, 49, 51,
                    52, 53, 55, 56, 57, 59, 60, 61, 63, 64, 65, 70, 72, 73, 75, 76, 77,
                    79, 80, 81, 84, 85, 86, 88, 89, 90],
                1: [1, 5, 9, 14, 18, 22, 27, 33, 37, 41, 46, 50, 54, 58, 62, 67, 74, 78, 82, 87]
            },
        "20-0m":
            {
                0: [2, 3, 4, 6, 7, 8, 10, 11, 13, 15, 16, 17, 19, 20, 21, 23, 24,
                    25, 28, 31, 32, 34, 35, 36, 38, 39, 40, 42, 43, 44, 47, 48, 49, 51,
                    52, 53, 55, 56, 57, 59, 60, 61, 63, 64, 65, 70, 72, 73, 75, 76, 77,
                    79, 80, 81, 84, 85, 86, 88, 89, 90],
                1: [1, 5, 9, 14, 18],
                2: [22, 27, 33, 37, 41],
                3: [46, 50, 54, 58, 62],
                4: [67, 74, 78, 82, 87]
            },
        "20-1":
            {
                0: [1, 3, 4, 5, 7, 8, 9, 11, 13, 14, 16, 17, 18, 20, 21, 22, 24,
                    25, 27, 31, 32, 33, 35, 36, 37, 39, 40, 41, 43, 44, 46, 48, 49, 50,
                    52, 53, 54, 56, 57, 58, 60, 61, 62, 64, 65, 67, 72, 73, 74, 76, 77,
                    78, 80, 81, 82, 85, 86, 87, 89, 90],
                1: [2, 6, 10, 15, 19, 23, 28, 34, 38, 42, 47, 51, 55, 59, 63, 70, 75, 79, 84, 88]
            },
        "20-1m":
            {
                0: [1, 3, 4, 5, 7, 8, 9, 11, 13, 14, 16, 17, 18, 20, 21, 22, 24,
                    25, 27, 31, 32, 33, 35, 36, 37, 39, 40, 41, 43, 44, 46, 48, 49, 50,
                    52, 53, 54, 56, 57, 58, 60, 61, 62, 64, 65, 67, 72, 73, 74, 76, 77,
                    78, 80, 81, 82, 85, 86, 87, 89, 90],
                1: [2, 6, 10, 15, 19],
                2: [23, 28, 34, 38, 42],
                3: [47, 51, 55, 59, 63],
                4: [70, 75, 79, 84, 88]
            },
        "20-2":
            {
                0: [1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 18, 19, 21, 22, 23,
                    25, 27, 28, 32, 33, 34, 36, 37, 38, 40, 41, 42, 44, 46, 47, 49, 50,
                    51, 53, 54, 55, 57, 58, 59, 61, 62, 63, 65, 67, 70, 73, 74, 75, 77,
                    78, 79, 81, 82, 84, 86, 87, 88, 90],
                1: [3, 7, 11, 16, 20, 24, 31, 35, 39, 43, 48, 52, 56, 60, 64, 72, 76, 80, 85, 89]
            },
        "20-2m":
            {
                0: [1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 18, 19, 21, 22, 23,
                    25, 27, 28, 32, 33, 34, 36, 37, 38, 40, 41, 42, 44, 46, 47, 49, 50,
                    51, 53, 54, 55, 57, 58, 59, 61, 62, 63, 65, 67, 70, 73, 74, 75, 77,
                    78, 79, 81, 82, 84, 86, 87, 88, 90],
                1: [3, 7, 11, 16, 20],
                2: [24, 31, 35, 39, 43],
                3: [48, 52, 56, 60, 64],
                4: [72, 76, 80, 85, 89]
            },
        "20-3":
            {
                0: [1, 2, 3, 5, 6, 7, 9, 10, 11, 14, 15, 16, 18, 19, 20, 22, 23,
                    24, 27, 28, 31, 33, 34, 35, 37, 38, 39, 41, 42, 43, 46, 47, 48, 50,
                    51, 52, 54, 55, 56, 58, 59, 60, 62, 63, 64, 67, 70, 72, 74, 75, 76,
                    78, 79, 80, 82, 84, 85, 87, 88, 89],
                1: [4, 8, 13, 17, 21, 25, 32, 36, 40, 44, 49, 53, 57, 61, 65, 73, 77, 81, 86, 90]
            },
        "20-3m":
            {
                0: [1, 2, 3, 5, 6, 7, 9, 10, 11, 14, 15, 16, 18, 19, 20, 22, 23,
                    24, 27, 28, 31, 33, 34, 35, 37, 38, 39, 41, 42, 43, 46, 47, 48, 50,
                    51, 52, 54, 55, 56, 58, 59, 60, 62, 63, 64, 67, 70, 72, 74, 75, 76,
                    78, 79, 80, 82, 84, 85, 87, 88, 89],
                1: [4, 8, 13, 17, 21],
                2: [25, 32, 36, 40, 44],
                3: [49, 53, 57, 61, 65],
                4: [73, 77, 81, 86, 90]
            },
    },

    "coco-stuff": {
        "offline":
            {
                0: list(range(1, 183)),
            },
        "spn":
            {  # labels are remapped according to http://github.com/nightrome/cocostuff/blob/master/labels.md
                0: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 27, 28, 31, 32, 35,
                    36, 37, 38, 39, 40, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63,
                    64, 65, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 88, 89, 90, 92, 93, 94, 95,
                    96, 97, 98, 99, 101, 102, 103, 104, 105, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
                    119, 120, 121, 122, 123, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139,
                    140, 141, 142, 143, 144, 146, 147, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162,
                    163, 164, 165, 166, 167, 168, 170, 171, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182],  # 156 cl
                1: [21, 25, 33, 34, 41, 57, 87, 100, 106, 124, 145, 148, 149, 169, 172]  # 15 cl not in ImageNet
            }
    }
}

def get_task_list():
    return [task for ds in tasks.keys() for task in tasks[ds].keys()]

class Task:
    def __init__(self, opts):
        self.step = opts.step
        self.dataset = opts.dataset
        self.task = opts.task
        if self.task not in tasks[self.dataset]:
            raise NotImplementedError(f"The task {self.task} is not present in {self.dataset}")
        self.task_dict = tasks[self.dataset][self.task]
        assert self.step in self.task_dict.keys(), f"You should provide a valid step! [{self.step} is out of range]"
        self.order = [cl for s in range(self.step + 1) for cl in self.task_dict[s]]

        self.disjoint = True

        self.nshot = opts.nshot if self.step > 0 else -1
        self.ishot = opts.ishot

        self.input_mix = opts.input_mix  # novel / both / seen

        self.num_classes = len(self.order)

        # add the background
        self.order.insert(0, 0)
        self.num_classes += 1

    def get_order(self):
        return self.order

    def get_future_labels(self):
        return [cl for s in self.task_dict.keys() for cl in self.task_dict[s] if s > self.step]

    def get_novel_labels(self):
        return list(self.task_dict[self.step])

    def get_old_labels(self, bkg=True):
        if bkg:
            return [0] + [cl for s in range(self.step) for cl in self.task_dict[s]]
        else:
            return [cl for s in range(self.step) for cl in self.task_dict[s]]

    def get_task_dict(self):
        return {s: self.task_dict[s] for s in range(self.step + 1)}

    def get_n_classes(self):
        r = [len(self.task_dict[s]) for s in range(self.step + 1)]
        # consider background
        r[0] += 1
        return r


def get_task_list():
    return [task for ds in tasks.keys() for task in tasks[ds].keys()]


class Task:
    def __init__(self, opts):
        self.step = opts.step
        self.dataset = opts.dataset
        self.task = opts.task
        if self.task not in tasks[self.dataset]:
            raise NotImplementedError(f"The task {self.task} is not present in {self.dataset}")
        self.task_dict = tasks[self.dataset][self.task]
        assert self.step in self.task_dict.keys(), f"You should provide a valid step! [{self.step} is out of range]"
        self.order = [cl for s in range(self.step + 1) for cl in self.task_dict[s]]

        self.disjoint = True

        self.nshot = opts.nshot if self.step > 0 else -1
        self.ishot = opts.ishot

        self.input_mix = opts.input_mix  # novel / both / seen

        self.num_classes = len(self.order)

        # add the background
        self.order.insert(0, 0)
        self.num_classes += 1

    def get_order(self):
        return self.order

    def get_future_labels(self):
        # not tested
        return [cl for s in self.task_dict.keys() for cl in self.task_dict[s] if s > self.step]

    def get_novel_labels(self):
        return list(self.task_dict[self.step])

    def get_old_labels(self, bkg=True):
        if bkg:
            return [0] + [cl for s in range(self.step) for cl in self.task_dict[s]]
        else:
            return [cl for s in range(self.step) for cl in self.task_dict[s]]

    def get_task_dict(self):
        return {s: self.task_dict[s] for s in range(self.step + 1)}

    def get_n_classes(self):
        r = [len(self.task_dict[s]) for s in range(self.step + 1)]
        # consider background
        r[0] += 1
        return r
