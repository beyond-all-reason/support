function gadget:GetInfo()
  return {
    name      = "Reject armspy orders",
    desc      = "Reject armspy orders",
    author    = "",
    date      = "",
    license   = "Tarquin Fin-tim-lin-bin-whin-bim-lim-bus-stop-F'tang-F'tang-Olé-Biscuitbarrel",
    layer     = 10,
    enabled   = true
  }
end

if (not gadgetHandler:IsSyncedCode()) then
  return false
end

local armSpyDID = UnitDefNames["armspy"].id

function gadget:AllowCommand(unitID, unitDefID, unitTeam, cmdID, cmdParams, cmdOptions, cmdTag, synced)
    if unitDefID==armSpyDefID and GG.MagicForest then
        return false
    end
    return true
end