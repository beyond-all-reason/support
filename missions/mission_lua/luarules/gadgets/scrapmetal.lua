function gadget:GetInfo()
  return {
    name      = "Resurrectabke wreck placer",
    desc      = "Resurrectabke wreck placer",
    author    = "beherith",
    date      = "July 2012",
    license   = "GNU GPL, v2 or later",
    layer     = 10,
    enabled   = true
  }
end

if (not gadgetHandler:IsSyncedCode()) then
  return false
end

function gadget:GameStart()
    if not GG.ScrapMetal then return end

   wreck=Spring.CreateFeature('shiva_dead', 3319, -104, 989) --x,y,z positions
   Spring.SetFeatureResurrect(wreck,'shiva')

   wreck=Spring.CreateFeature('corcom_dead', 2128, 188, 2378) --x,y,z positions
   Spring.SetFeatureResurrect(wreck,'corcom')

   wreck=Spring.CreateFeature('armraven_dead', 3810, 100, 3334) --x,y,z positions
   Spring.SetFeatureResurrect(wreck,'armraven')

   wreck=Spring.CreateFeature('coracv_dead', 691, 96, 1040) --x,y,z positions
   Spring.SetFeatureResurrect(wreck,'coradv')

   wreck=Spring.CreateFeature('corbats_dead', 332, -21, 4020) --x,y,z positions
   Spring.SetFeatureResurrect(wreck,'corbats')
end