class Node(): #Node for doubly linked list with two data inputs
    def __init__(self, item):
        self.item = item
        self.data = None
        self.data2 = None
        self.next = None
        self.prev = None
        self.search = None

class DLinkedList(): #Class for double linked list
    def __init__(self):
        self.head = None


    def push_item(self, item): #pushes item into linked list
        new_node = Node(item)
        new_node.next = self.head
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node


    def remove_last_item(self): #removes the last item added to list
        if self.head == None:
            return(print("the list is empty."))
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        new_last = last_node.prev
        new_last.next = None

    def remove_item(self,item): #removes specified item
        node = self.head
        while (node.item is not item):
            node = node.next
        print(node, 'here')
        prev_node = node.prev
        next_node = node.next
        if next_node == None:
            prev_node.next = None
        elif prev_node==None:
            self.head = next_node
        else:
            prev_node.next = next_node
            next_node.prev = prev_node

    def insert_item(self, item, prev_item): #inserts item after prev_item
        print(item, prev_item)
        prev_node = self.find_item(prev_item,0)

        next_node = prev_node.next
        new_node = Node(item)

        prev_node.next = new_node
        next_node.prev = new_node

        new_node.next = next_node
        new_node.prev = prev_node

    def print_list(self):
        node = self.head
        while(node is not None):
            print(node.item)
            node = node.next

    def find_item(self, item, x): #finds item in list
        node = self.head
        if item == None:
            return print("No node found")

        while node.item != item:
            node=node.next
            if node.item == None:
                return print("No value found.")
        if x == 0:
             return node
        elif x ==1:
            return (node.item, node.data, node.data2)

    def add_data(self,data): #adds data to head
        self.head.data = data

    def change_data(self,item,data): #changes data of specific item
        node = self.find_item(item,0)
        node.data = data

    def add_data2(self,data): #adds data2 to head
        self.head.data2 = data

    def change_data2(self,item,data): #changes data2 of specific item
        node = self.find_item(item,0)
        node.data2 = data

    def data_retrival(self): #returns data of items, in order they were added
        node = self.head
        value_list = []
        while(node.next is not None):
            node = node.next
        while (node is not None):
            value_list.append(node.item)#NEEDS REWORK
            value_list.append(node.data)
            node = node.prev
        print(value_list)
        return value_list

    def len(self):
        len = 0
        node = self.head
        while (node is not None):
            len += 1
            node = node.next
        print(len)
        return len

    def return_head(self):
        return self.head

    #################testing###################

    def print_list_data(self):
        node = self.head
        price_list = []
        item_list= []
        while (node is not None):
            item = node.item.get()
            price = node.data.get()
            price_list.append(price)
            item_list.append(item)
            node = node.next

        lists = (item_list, price_list)


        return lists





def test():
        testnode = Node(12)
        testlist = DLinkedList()
        testlist.print_list()
        testlist.push_item(5)
        testlist.push_item(10)
        testlist.push_item(15)
        testlist.push_item(20)
        testlist.add_data("Tree")
        testlist.add_data2('pigs')
        testlist.print_list()
        testlist.remove_item(10)
        testlist.print_list()
        testlist.remove_last_item()
        testlist.print_list()
        testlist.find_item(15,0)
        testlist.insert_item(12, 20)
        testlist.print_list()

        testlist.change_data(15,"green")
        testlist.data_retrival()

        testlist.len()

test()