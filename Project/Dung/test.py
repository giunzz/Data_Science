class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class LikedList:
    def __init__(self):
        self.head = None
        self.tail = None
  def insert(self,x):
    p = Node(x)
    if self.head == None:
    		self.head = seld.tail = p
    else:
      	self.tail.next = p
        self.tail = p
  def min(self):
    if self.head == None:
      	return None
    cur = ans = self.head
    while cur:
      	if cur.data < ans.data:
          	ans = cur
        cur = cur.next
    return ans
#main  
lst = LikedList()
while True: 
  x = int(input())
  if x == 0:
    break
  lst.insert(x)
ans = lst.min()
if ans: 
  print(ans.data)
else:
  print(0)