import copy
class Region:
    def __init__(self, name):
        self.name = name
        self.adjacent = []
        self.domain_values = []
        # value is the color assigned to the region
        self.value = ""
        # count is to keep track of unassigned neighbors
        self.count = 0


def read_file():
    # read input file
    file = open("Input2.txt")
    dom_val = []
    num_var, num_dom_val, count, line = 0, 0, 0, 0
    regions = []
    adjacent = {}
    assignment = {}
    for i in file:
        x = i.split()
        # first line
        if line == 0:
            num_var = x[0]
            num_dom_val = x[1]
        # second line is name
        # make class Region for every region
        elif line == 1:
            for j in range(len(x)):
                name = Region(x[j])
                regions.append(name)
                # make dictionary --> every region is key
                # values of key would be the adjacent regions
                adjacent[x[j]] = []
                # diction to assign value to region
                assignment[x[j]] = []
        # every Region has domain values listed in line 2
        elif line == 2:
            dom_val = x
            for j in regions:
                for clr in x:
                    j.domain_values.append(clr)
        else:
            if count < len(regions):
                for j in range(len(x)):
                    if x[j] == '1':
                        regions[count].adjacent.append(regions[j].name)
                        # add values of neighbors to key
                        region = regions[count].name
                        adjacent[region].append(regions[j].name)
                count += 1
        line += 1
    file.close()
    return regions, num_var, num_dom_val, dom_val, adjacent, assignment


def output_file(result):
    file = open("Output2.txt", "w")
    # i just need to write region and assigned color to new file
    for key, val in result.items():
        file.write(key + ' = ' + val + "\n")


def select_unassigned_variable(regions, assignment):
    # minimum remaining value heuristic
    mrv = []
    # need to get regions that are not assigned
    for region in regions:
        # if not assigned, add to unassigned list
        if not assignment[region.name]:
            mrv.append(region)
    # --> sorts by how many values are left in domain
    mrv.sort(key=lambda x: len(x.domain_values))
    # if len of domain values of first and last element are the same after sort
    # means amount of values to pick are all the same
    # do degree heuristic
    if len(mrv[0].domain_values) != len(mrv[-1].domain_values):
        return mrv[0]
    # else apply degree heuristic
    degree = []
    for region in regions:
        # reset the count of unassigned neighbors
        region.count = 0
        # if region has been assigned
        if not assignment[region.name]:
            # for every neighbor not in assignment, get rid of assigned value
            for adj in region.adjacent:
                if not assignment[adj]:
                    # to keep track of unassigned neighbors in case need for degree heuristic
                    region.count += 1
    for region in regions:
        if not assignment[region.name]:
            degree.append(region)
    # sort by most unassigned neighbors
    degree.sort(key=lambda x : x.count, reverse=True)
    return degree[0]


def consistent(region, regions, assignment, adjacent):
    # for every neighbor, check if assigned
    # if assigned, check if have same colors, if so return False
    # else return True
    for neighbor in adjacent[region.name]:
        # if neighbor is assigned
        if assignment[neighbor]:
            # check to see if neighbor and region has same value
            if assignment[neighbor] == region.value:
                return False
    # passed the consistent check
    # update domain values of all neighbors
    clr = assignment[region.name]
    # go through every neighbor
    for neighbor in adjacent[region.name]:
        # find neighbor
        for i in regions:
            if i.name == neighbor and clr in i.domain_values:
                # remove clr from neighbor's domain
                i.domain_values.remove(clr)
    return True


def backtrack(regions, assignment, adjacent):
    count = 0
    # if assignment is complete, then return assignment
    for val in assignment.values():
        # meaning unassigned
        if not val:
            continue
        else:
            count += 1
    # if all regions are assigned, return
    if count == len(regions):
        return assignment
    # else select-unassigned-variable from the region
    region = select_unassigned_variable(regions, assignment)

    # for every color available in the selected unassigned region
    for value in region.domain_values:
        # copy in case it returns None then move on
        local_assignment = copy.deepcopy(assignment)
        # assign first color in domain
        local_assignment[region.name] = value
        # check to see if constraints are still consistent
        if consistent(region, regions, local_assignment, adjacent):
            # if consistent, return updated assignment
            result = backtrack(regions, local_assignment, adjacent)
            if result is not None:
                return result
    return None


def main():
    regions, num_var, num_dom_val, dom_val, adjacent, assignment = read_file()
    result = backtrack(regions, assignment, adjacent)
    output_file(result)


main()
