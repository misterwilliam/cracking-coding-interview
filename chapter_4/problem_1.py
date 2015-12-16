import functools
import unittest

class Node(object):

  def __init__(self, data, left=None, right=None):
    self.data = data
    self.left = left
    self.right = right

  def __repr__(self):
    if self.left is not None or self.right is not None:
      return "(%s %s %s)" % (self.data,
                             str(self.left) if self.left is not None else "-",
                             str(self.right) if self.right is not None else "-")
    else:
      return "(%s)" % self.data

class Continuation(object):

  def __init__(self, func):
    self.func = func

def is_balanced(root):
  # Definition of balanced is that left and right subtree's height do not differ by more
  # than one. This is a slightly weird definition, but whatever.
  left_height = get_height(root.left) if root.left is not None else 0
  right_height = get_height(root.right) if root.right is not None else 0

def iterative_dfs(root, onNode=None, onExit=None):
  todo = [root]
  while len(todo) > 0:
    current = todo.pop()
    if isinstance(current, Continuation):
      current.func()
    else:
      if onNode is not None:
        onNode(current)
      if onExit is not None:
        todo.append(Continuation(functools.partial(onExit, current)))

      if current.right is not None:
        todo.append(current.right)
      if current.left is not None:
        todo.append(current.left)

def rec_get_height(root, onNode=None):
  if onNode is not None:
    onNode(root)
  left_height, right_height = 0, 0
  if root.left is not None:
    left_height = rec_get_height(root.left)
  if root.right is not None:
    right_height = rec_get_height(root.right)
  return 1 + max(left_height, right_height)


class NodeTests(unittest.TestCase):

  def test_repr(self):
    root = Node("a",
                Node("b",
                  Node("d"),
                  Node("e")),
                Node("c"))
    self.assertEqual(str(root), "(a (b (d) (e)) (c))")

class GetHeightTests(unittest.TestCase):

  def test_rec_get_height_single_node(self):
    root = Node("a")
    self.assertEqual(rec_get_height(root), 1)

  def test_rec_get_height_two_nodes(self):
    root = Node("a", Node("b"))
    self.assertEqual(rec_get_height(root), 2)

  def test_rec_get_height(self):
    root = Node("a",
                Node("b",
                  Node("d"),
                  Node("e")),
                Node("c"))
    self.assertEqual(rec_get_height(root), 3)

class StackLogger(object):

  def __init__(self):
    self.stack = []
    self.stack_log = []

  def onNode(self, node):
    self.stack.append(node)

  def onExit(self, node):
    current_stack = [node.data for node in self.stack]
    self.stack_log.append(current_stack)
    self.stack.pop()

class IterativeDfsTest(unittest.TestCase):

  def test_simple(self):
    log = []
    def log_visits(node):
      log.append(node.data)

    root = Node("a",
            Node("b",
              Node("d"),
              Node("e")),
            Node("c",
              Node("f"),
              Node("g")))
    iterative_dfs(root, onNode=log_visits)
    self.assertEqual(log, ["a", "b", "d", "e", "c", "f", "g"])

  def test_on_exit(self):
    log = []
    def log_visits(node):
      log.append(node.data)

    root = Node("a",
            Node("b",
              Node("d"),
              Node("e")),
            Node("c",
              Node("f"),
              Node("g")))
    iterative_dfs(root, onExit=log_visits)
    self.assertEqual(log, ["d", "e", "b", "f", "g", "c", "a"])

  def test_stack_log(self):
    stack_logger = StackLogger()

    root = Node("a",
            Node("b",
              Node("d"),
              Node("e")),
            Node("c",
              Node("f"),
              Node("g")))
    iterative_dfs(root, onNode=stack_logger.onNode, onExit=stack_logger.onExit)
    self.assertEqual(stack_logger.stack_log,
                    [['a', 'b', 'd'],
                     ['a', 'b', 'e'],
                     ['a', 'b'],
                     ['a', 'c', 'f'],
                     ['a', 'c', 'g'],
                     ['a', 'c'],
                     ['a']])

if __name__ == "__main__":
  unittest.main()