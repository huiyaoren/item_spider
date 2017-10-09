from ebay.utils.data import insert_items_into_mysql

# fixme-已弃用

def run(day=None):
    insert_items_into_mysql(day)


if __name__ == '__main__':
    run()
