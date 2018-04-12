import Foundation

class Util {

//    min -> max inclusive
    static func randInt(min: Int, max: Int) -> Int {
        return Int(arc4random_uniform(UInt32(max - min))) + min
    }
}