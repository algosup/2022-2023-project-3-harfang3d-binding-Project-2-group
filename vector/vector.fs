type Vector2(x:float, y:float) =
    member this.X = x
    member this.Y = y
    member this.DistanceTo(pos:Vector2) = 
        sqrt( (pos.Y - this.Y) * (pos.Y - this.Y) + (pos.X - this.X) * (pos.X - this.X))
    member this.VectorMovement(plusx:float, plusy:float) = 
        this.X <- this.X + plusx
        this.Y <- this.Y + plusy
    member this.Midpoint(pos:Vector2) = 
        let mx = (this.X + pos.X) / 2.0
        let my = (this.Y + pos.Y) / 2.0
        Vector2(mx, my)
    member this.PercentDistance(pos:Vector2, percentOfDistance:float) = 
        this.DistanceTo(pos) / (100.0 / percentOfDistance)

type Vector3(x:float, y:float, z:float) =
    inherit Vector2(x, y)
    member this.Z = z
    override this.DistanceTo(pos:Vector3) = 
        sqrt( (pos.Y - this.Y) * (pos.Y - this.Y) + (pos.X - this.X) * (pos.X - this.X) + (pos.Z - this.Z) * (pos.Z - this.Z))
    override this.VectorMovement(plusx:float, plusy:float, plusz:float) = 
        base.VectorMovement(plusx, plusy)
        this.Z <- this.Z + plusz
    override this.Midpoint(pos:Vector3) = 
        let mx = (this.X + pos.X) / 2.0
        let my = (this.Y + pos.Y) / 2.0
        let mz = (this.Z + pos.Z) / 2.0
        Vector3(mx, my, mz)
    override this.PercentDistance(pos:Vector3, percentOfDistance:float) = 
        base.PercentDistance(pos, percentOfDistance)