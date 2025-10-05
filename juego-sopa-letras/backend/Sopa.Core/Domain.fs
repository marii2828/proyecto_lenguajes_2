namespace Sopa.Core

type Coord = { r:int; c:int }
type Grid = string[]
type Path = Coord list

type Placement = { word:string; path:Path }