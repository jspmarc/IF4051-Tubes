class TemperatureHistrogramUtils(object):
    @staticmethod
    def print_histogram(time, rdd) -> None:
        c = rdd.collect()
        print("-------------------------------------------")
        print("Time: %s" % time)
        print("-------------------------------------------")
        for record in c:
            # "draw" our lil' ASCII-based histogram
            print(str(record[0]) + ': ' + '#'*record[1])
        print("")