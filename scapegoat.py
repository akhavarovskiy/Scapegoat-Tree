import math
import sys

##########################################################################
# ScapeGoateTreeNode
##########################################################################
# Data of a single node of a scapegoat tree

class ScapeGoatTreeNode(object):
	##########################################################################
	# constructor()
	##########################################################################	
	def __init__( self, key : int ):
		self.key    = key
		self.left   = None
		self.right  = None
		self.parent = None

	##########################################################################
	# insert()
	##########################################################################	
	def insert( self, key : int ):
		# Base case to exit recurtion
		if self.key == key: 
			return None

		elif (self.key > key):
			if self.left is not None:
				return self.left.insert( key ) # = self.left.insert( key )
			else:
				self.left = ScapeGoatTreeNode( key )
				self.left.parent = self
				return self.left

		elif self.key < key: 
			if self.right is not None:
				return self.right.insert( key ) #= self.right.insert( key )
			else:
				self.right = ScapeGoatTreeNode( key )
				self.right.parent = self
				return self.right

		return None

	##########################################################################
	# delete()
	##########################################################################
	def delete( self, key : int ):
		#If we are at the leaf node and its null the element does not exist within the tree
		if self is None:
			return None

		if self.key > key:
			if self.left is not None:
				self.left = self.left.delete( key )
		
		elif self.key < key:
			if self.right is not None:
				self.right = self.right.delete( key )

		else:
			if self.left is None:
				temp        = self.right
				if temp is not None:
					temp.parent = self.parent
				self        = None
				return temp

			elif self.right is None:
				temp        = self.left
				if temp is not None:
					temp.parent = self.parent
				self        = None
				return temp
			
			temp       = self.right.__minKeyNode()
			self.key   = temp.key
			self.right = self.right.delete( temp.key )

		return self

	##########################################################################
	# __minKeyNode() - Internal, used for deleting elements from the tree
	##########################################################################
	# Grab the minimum left node of the subtree
	def __minKeyNode( self ):
		iter_node = self
		while not ( iter_node.left is None ):
			iter_node = iter_node.left

		return iter_node

	##########################################################################
	# search()
	##########################################################################
	# Look for a node in the current subtree
	def search( self, key : int ):
		if self.key == key:
			return self
		
		elif self.key > key:
			if self.left is not None:
				return self.left.search( key )
			else:
				return None
		elif self.key < key:
			if self.right is not None:
				return self.right.search( key )
			else:
				return None

	##########################################################################
	# height()
	##########################################################################
	# Get the height of the tree 
	def height( self ):
		left = 0
		right = 0

		if self.left is not None: 
			left = self.left.height() 
		
		if self.right is not None:
			right = self.right.height() 

		return 1 + max( left, right )

	##########################################################################
	# size()
	##########################################################################
	def size( self ):
		if self.left is None and self.right is None:
			return 1

		leftSize  = self.left.size() if self.left else 0
		rightSize = self.right.size() if self.right else 0

		return 1 + leftSize + rightSize 
	##########################################################################
	# depth()
	##########################################################################
	# Depth of the tree. IE, number of edges to the selected key
	def depth( self, key : int ):
		if self is None:
			raise ValueError( 'ScapegoatTree::depth(%d) The key does not exist within the tree' % key )
		
		if key < self.key:
			return 1 + self.left.depth( key )
		elif key > self.key:
			return 1 + self.right.depth( key )
		else:
			return 0

	##########################################################################
	# flatten()
	##########################################################################
	# Essentially LNR while building a list. 
	def flatten( self, flatTree ):
		if self.left  is not None: 
			self.left.flatten( flatTree ) 
		flatTree.append(self.key)
		if self.right is not None: 
			self.right.flatten( flatTree )

	##########################################################################
	# alphaHeight()
	##########################################################################
	# Alpha height
	def alphaHeight( self, alpha : float ):
		return math.floor( math.log( self.size(), 1.0/alpha ) + 1 )

	##########################################################################
	# alphaWeightBallanced()
	##########################################################################
	# Alpha weight ballanced
	def alphaWeightBallanced( self, alpha : float ):
		return self.left.size()  <= alpha*self.size() and \
			   self.right.size() <= alpha*self.size()

	##########################################################################
	# alphaHeightBallanced()
	##########################################################################
	# Alpha height ballanced
	def alphaHeightBallanced( self, alpha : float ):
		return self.height() <= self.alphaHeight( alpha )


##########################################################################
# ScapeGoateTree
##########################################################################
# Python implimentation of a scapegoat tree
class ScapeGoatTree(object):

	##########################################################################
	#  __init__()
	##########################################################################
	# Constructor
	def __init__ ( self, alpha : float, key : int ):
		if alpha >= 1.0 or alpha < 0.5:
			raise ValueError( 'ScapegoatTree(): Invalid alpha value: 0.5 <= alpha < 1' )

		self.__root             = ScapeGoatTreeNode( key )
		self.__treeAlpha        = alpha
		self.__treeMaxSize      = 1

	##########################################################################
	# insert()
	##########################################################################	
	def insert( self, key : int ):
		if self.__root is None:
			self.__root      = ScapeGoatTreeNode( key )
			return

		x = self.__root.insert( key )

		if x is None:
			return

		elif self.__root.depth( x.key ) > self.__root.alphaHeight( self.__treeAlpha ):
			flatTree = list()
			scapegoat = self.findScapegoat( x )
			scapegoat.flatten( flatTree )
			node      = self.buildHeightBalancedTree( flatTree )
			
			if scapegoat is self.__root:
				self.__root = node
			else:
				if scapegoat.parent.left == scapegoat:
					scapegoat.parent.left = node
					node.parent           = scapegoat.parent

				if scapegoat.parent.right == scapegoat:
					scapegoat.parent.right = node
					node.parent            = scapegoat.parent
				
		self.__treeMaxSize = max( self.__root.size(), self.__treeMaxSize )
	##########################################################################
	# delete()
	#########################################################################
	# 
	def delete( self, key ):
		if self.__root is None:
			return False

		self.__root = self.__root.delete( key )		
		if self.__root is None:
			return True

		self.__root.parent = None

		if  self.__root.size() < ( self.__treeAlpha* self.__treeMaxSize ):
			flatTree = list()
			self.__root.flatten( flatTree ) 

			self.__root = self.buildHeightBalancedTree( flatTree )
			self.__treeMaxSize = self.size()
			
		return True

	##########################################################################
	# search()
	#########################################################################
	# Returns the node with the given key, returns none if node dosent exist
	def search( self, key : int ):
		if self.__root is None:
			return False

		return self.__root.search( key )

	##########################################################################
	# height()
	##########################################################################
	# Get the height of the tree 
	def height( self ):
		if self.__root is None:
			return 0

		return self.__root.height()

	##########################################################################
	# size()
	##########################################################################
	# Number of elements within the tree 
	def size( self ):
		if self.__root is None:
			return 0
			
		return self.__root.size()
	
	##########################################################################
	# depth()
	##########################################################################
	# Depth of the tree. IE, number of edges to the selected key
	def depth( self, key : int ):
		if self.__root is None:
			return None

		return self.__root.depth( key )

	##########################################################################
	# findScapegoat()
	##########################################################################
	def findScapegoat( self, node : ScapeGoatTreeNode ):
		size   = 1
		height = 0

		iter = node
		while iter is not None:
			# Are we the left child?
			if iter == iter.parent.left: sibling = iter.parent.right
			# Are we the right child?
			if iter == iter.parent.right: sibling = iter.parent.left

			height    = height + 1
			totalSize = 1 + size + (sibling.size() if sibling is not None else 0)

			if height > math.floor( math.log( totalSize, 1/self.__treeAlpha ) + 1 ):
				return iter.parent
			
			iter = iter.parent
			size = totalSize
		
		return None

	
	##########################################################################
	# buildHeightBalancedTree()
	##########################################################################
	def buildHeightBalancedTree(self, treeList : list):
		if len( treeList ) == 0:
			return None

		if len( treeList ) == 1:
			return ScapeGoatTreeNode( treeList[ 0 ] )
		
		elif len( treeList ) == 2:
			node              = ScapeGoatTreeNode( treeList[ 0 ] )
			node.right        = ScapeGoatTreeNode( treeList[ 1 ] )
			node.right.parent = node
			return node
		
		center = int(math.floor((len( treeList ))/2)) 

		root              = ScapeGoatTreeNode( treeList[ center ] )
		root.left         = self.buildHeightBalancedTree( treeList[  :center ] )

		root.left.parent  = root
		root.right        = self.buildHeightBalancedTree( treeList[  (center + 1): ] )
		root.right.parent = root

		return root
