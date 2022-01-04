from xmldiff import main, formatting

def compare_xml(tree1, tree2):
    """Compare two XML trees."""
    tree_diff = main.diff_trees(left=tree1,
                                right=tree2,
                                formatter = formatting.DiffFormatter(pretty_print=True))
    if len(tree_diff) == 0:
        return True
    else:
        print('==== Start Differences ====')
        print(tree_diff)
        print('===== End Differences =====')
        return False