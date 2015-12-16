import unittest

class Node(object):

  def __init__(self, data, children=None):
    self.data = data
    if children is None:
      self.children = []
    else:
      self.children = children

def is_connected(a, b):
  todo = [a]
  seen = set(todo)
  while len(todo) > 0:
    current = todo.pop()  # DFS
    if current is b:
      return True
    for child in current.children:
      if child not in seen:
        seen.add(child)
        todo.append(child)
  return False

class IsConnectedTests(unittest.TestCase):

  def test_is_connected(self):
    a = Node("a")
    b = Node("b")
    c = Node("c")
    a.children.append(b)
    b.children.append(c)
    c.children.append(a)
    self.assertTrue(is_connected(a, c))

  def test_is_not_connected(self):
    a = Node("a")
    b = Node("b")
    self.assertFalse(is_connected(a, b))

  def test_does_not_get_stuck_in_loops(self):
    # Create loop
    a = Node("a")
    b = Node("b")
    c = Node("c")
    a.children.append(b)
    b.children.append(c)
    c.children.append(a)

    d = Node("d")
    self.assertFalse(is_connected(a, d))

if __name__ == "__main__":
  unittest.main()