import pygame as pg
import globals as globe

class Grid(object):
	def __init__(self):
		self.res = (600,400) # The dimension of the surface
		self.pix = (100,100) # Number of pixels on screen/board/canvas
		self.zoom_off = [0.0, 0.0] # The zoomed offset
		self.grid = pg.Surface(self.res)
		self.zoom_factor = 1.0

		# Creating the matrix
		self.pix_matrix = [[0 for x in range(self.pix[0])] for y in range(self.pix[1])] 

		# Initialize the matrix now.
		for row in range(0,self.pix[1]):
			for col in range(0,self.pix[0]):
				self.pix_matrix[row][col] = 0

		self.pix_matrix[1][0] = 1 # Testing

		# Drawing stuff
		self.redraw_canvas()

	def redraw_canvas(self):
		self.calc_dim()
		self.key = (249, 17, 17) # The Color Key
		self.grid.fill(self.key)
		self.grid.set_colorkey(self.key)
		self.grid.set_alpha(255)
		self.drawRects()
		self.drawLines() # Draws the lines onto the surface.

	def calc_dim(self):
		# Fit to screen
		#self.pix_dim = (self.res[0] / self.pix[0], self.res[1] / self.pix[1])
		num = int(globe.DEFAULT_PIXEL_SIZE * self.zoom_factor)
		if num <= 0:
			num = 1
		self.pix_dim = [num, num]

	def mouse_click(self, pos, offset=(0,0)):
		pos = self.pos_to_pix(pos)
		x, y = pos[0], pos[1]
		if x != -1 and y != -1:
			self.pix_matrix[y][x] = 1
			self.redraw_canvas()

	def zoom(self, pos, isZoomIn):
		self.before_zoom = self.zoom_factor
		zoom = 1.1

		if isZoomIn == True:
			self.zoom_factor *= zoom
		else:
			self.zoom_factor /= zoom

		if self.zoom_factor > globe.MAX_ZOOM_IN:
			self.zoom_factor = globe.MAX_ZOOM_IN
		if self.zoom_factor < globe.MAX_ZOOM_OUT:
			self.zoom_factor = globe.MAX_ZOOM_OUT

		scalechange = self.zoom_factor - self.before_zoom
		if scalechange != 0:
			#pan_x = -(pos[0] / (self.zoom_factor*zoom) - pos[0]/self.zoom_factor)
			#pan_y = -(pos[1] / (self.zoom_factor*zoom) - pos[1]/self.zoom_factor)
			pan_x = -(pos[0] * scalechange)
			pan_y = -(pos[1] * scalechange)
			print "X: ", pan_x, " Y: ", pan_y
			self.pan((pan_x, pan_y))

		self.redraw_canvas()

	def zoom_in(self, pos, amount=1):
		self.zoom(pos, True)

	def zoom_out(self, pos, amount=1):
		self.zoom(pos, False)

	def pan(self, delta):
		self.zoom_off[0] += delta[0]
		self.zoom_off[1] += delta[1]
		print "Zoom Off: ", self.zoom_off
		self.redraw_canvas()

	def pos_to_pix(self, pos):
		x = int((pos[0] - self.zoom_off[0]) / self.pix_dim[0])
		y = int((pos[1] - self.zoom_off[1]) / self.pix_dim[1])
		if x >= self.pix[0] or x < 0:
			x = -1
		if y >= self.pix[1] or x < 0:
			y = -1

		return (x, y)

	def drawRects(self):
		colors = ((0,0,0,255)) # One color right now, green
		for row in range(0,self.pix[1]):
			for col in range(0,self.pix[0]):
				val = self.pix_matrix[row][col]
				if val == 1:
					pos = (col * self.pix_dim[0] + self.zoom_off[0], row * self.pix_dim[1] + self.zoom_off[1])
					r = pg.Rect(pos, self.pix_dim)
					pg.draw.rect(self.grid, colors[0], r)
					#self.grid.fill(colors[0], r)

	def drawLines(self):
		if self.zoom_factor < globe.GRID_ZOOM_GONE:
			return

		color = (0,0,0,240)
		width = 1
		lens = (self.pix_dim[0] * self.pix[0], self.pix_dim[1] * self.pix[1])
		incs = (self.pix_dim[0], self.pix_dim[1])

		for y in xrange(0, lens[1] + 1, incs[1]): # Horizontal lines
			tup1 = (0 + self.zoom_off[0]          , y + self.zoom_off[1])
			tup2 = (lens[0] + self.zoom_off[0], y + self.zoom_off[1])
			pg.draw.line(self.grid, color, tup1, tup2, width)

		for x in xrange(0, lens[0] + 1, incs[0]): # Vertical lines
			tup1 = (x + self.zoom_off[0], 0 + self.zoom_off[1]          )
			tup2 = (x + self.zoom_off[0], lens[1] + self.zoom_off[1])
			pg.draw.line(self.grid, color, tup1, tup2, width)

	def draw(self, screen):
		screen.blit(self.grid, (0,0))
