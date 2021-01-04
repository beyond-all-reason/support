

local Base = {
	description = "Orange Mushrooms",

	footprintx = 2,
	footprintz = 2,
	blocking = false,
	upright = false,
	category =  "vegetation",
	reclaimable			= true,
	autoreclaimable		= true, 	

	metal = 0,
	energy = 100,
	
	height				= "20",
	damage = 250,

	customparams = {
		author = "Lathan",
		category = "mushroom",
		set = "Lathan's Mushrooms",
		normalmaps = "yes",
		normaltex = "unittextures/shroomorange_normal.png",
		treeshader = "no",
		randomrotate = "true",
	},
}

local mushrooms = {}
for i = 1, 9 do
	local name = "mushroom0" .. i
	local def = {}
	for k, v in pairs(Base) do
		def[k] = v
	end
	def.name = name
	def.object =  name .. ".s3o"
	mushrooms[name] = def
end

return mushrooms
