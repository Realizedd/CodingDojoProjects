import SpriteKit
import CoreMotion

class GameScene: SKScene {
    
    let motionManager = CMMotionManager()
    
    var moving: SKNode?
    
    var timer: SKLabelNode?
    var status: SKLabelNode?
    var gameOver: SKLabelNode?
    var player: SKShapeNode?
    var bars = [SKNode]()
    
    var timeSurvived = 0.0
    var lastUpdate: NSDate?
    
    var running = false
    
    override func didMoveToView(view: SKView) {
        timer = SKLabelNode(fontNamed: "Chalkduster")
        timer?.fontSize = 13.0
        timer?.fontColor = UIColor.whiteColor()
        timer?.text = "Time: 0.0s"
        timer?.position = CGPointMake(self.frame.width - 50, self.frame.height - 30)
        self.addChild(timer!)
        
        gameOver = SKLabelNode(fontNamed: "Chalkduster")
        gameOver?.fontSize = 17.0
        gameOver?.fontColor = UIColor.redColor()
        gameOver?.position = CGPointMake(self.frame.width / 2, self.frame.height / 2 + 40)
        gameOver?.hidden = true
        self.addChild(gameOver!)
        
        status = SKLabelNode(fontNamed: "Chalkduster")
        status?.fontSize = 15.0
        status?.fontColor = UIColor.whiteColor()
        status?.text = "TOUCH THE SCREEN TO START"
        status?.position = CGPointMake(self.frame.width / 2, self.frame.height / 2)
        self.addChild(status!)
        
        motionManager.deviceMotionUpdateInterval = 1 / 60.0
        
        motionManager.startDeviceMotionUpdatesToQueue(NSOperationQueue.mainQueue(), withHandler: {
            data, error in
            let angleDegrees = (atan2((data?.gravity.y)!, (data?.gravity.x)!) + M_PI_2) * 180.0 / M_PI
            self.player?.physicsBody?.applyImpulse(CGVectorMake(CGFloat(angleDegrees), 0))
        })
        
        self.physicsBody = SKPhysicsBody(edgeLoopFromRect: CGRectMake(self.frame.origin.x, self.frame.origin.y - 30, self.frame.size.width, self.frame.size.height + 30))
        self.physicsWorld.gravity = CGVectorMake(0.0, -10.0)
        self.backgroundColor = UIColor(red: 113.0 / 255.0, green: 197.0 / 255.0, blue: 207.0 / 255.0, alpha: 1.0)
        
        moving = SKNode()
        self.addChild(moving!)
    }
    
    func startGame() {
        running = true
        let shape = SKShapeNode(circleOfRadius: 15.0)
        player = shape
        shape.position = CGPoint(x: CGRectGetMidX(frame) + 100.0, y: CGRectGetMidY(frame))
        shape.fillColor = UIColor.orangeColor()
        shape.physicsBody = SKPhysicsBody(circleOfRadius: 15.0)
        shape.physicsBody?.dynamic = true
        shape.physicsBody?.affectedByGravity = true
        shape.physicsBody?.allowsRotation = true
        shape.physicsBody?.mass = 0.0
        moving?.addChild(shape)
        
        let spawn = SKAction.performSelector(#selector(spawnBars), onTarget: self)
        let delay = SKAction.waitForDuration(0.5)
        let spawnThenDelay = SKAction.sequence([spawn, delay])
        let spawnThenDelayForever = SKAction.repeatActionForever(spawnThenDelay)
        self.runAction(spawnThenDelayForever, withKey: "barGeneration")
    }
    
    func spawnBars() {
        let spaceBetween: CGFloat = 50.0 // The actual spacing
        
        let bar = SKNode() // The wrapper for bar parts
        
        bar.position = CGPointMake(0, -(self.frame.height / 20)) // Starts from the bottom, to slide up to maxY + barHeight
        
        let spacing = arc4random_uniform(UInt32(3)) + 1 // How many spacings should a bar have?
        
//        Base Idea: 
//        Generate random sized 3 bar parts that lengths in total = frameWidth / 2
//        While generating them, decide RANDOMLY which bar part will have a random spacing.
//        Subtract the spacing from the width, subtract 1 from spacing variable.
        
        var maxWidth = self.frame.width / 2
        
        var x = 0
        
        for i in 1...3 {
            
        }
        
        let randomWidth = 2.0 - (CGFloat(arc4random_uniform(UInt32(5))) / 10.0)

        let right = SKShapeNode(rect: CGRectMake(0, 0, (self.frame.width / randomWidth) - spaceBetween, self.frame.height / 20))
        right.fillColor = UIColor.redColor()
        right.physicsBody = SKPhysicsBody(edgeLoopFromRect: CGRectMake(0, 0, (self.frame.width / randomWidth)  - spaceBetween, self.frame.height / 20))
        right.physicsBody?.dynamic = true
        bar.addChild(right)
        
        let left = SKShapeNode(rect: CGRectMake(0, 0, self.frame.width / (4.0 - randomWidth), self.frame.height / 20))
        left.fillColor = UIColor.blueColor()
        left.position = CGPointMake(right.position.x + right.frame.width + spaceBetween, right.position.y)
        left.physicsBody = SKPhysicsBody(edgeLoopFromRect: CGRectMake(0, 0, self.frame.width / (4.0 - randomWidth), self.frame.height / 20))
        left.physicsBody?.dynamic = true
        bar.addChild(left)
        
        moving?.addChild(bar)
        
        let moveToTop = SKAction.moveTo(CGPointMake(0, self.frame.maxY), duration: 3)
        bar.runAction(moveToTop)
        bars.append(bar)
    }
    
    override func touchesBegan(touches: Set<UITouch>, withEvent event: UIEvent?) {
        if !running {
            timeSurvived = 0.0
            lastUpdate = NSDate()
            status?.hidden = true
            gameOver?.hidden = true
            startGame()
        }
    }
   
    override func update(currentTime: CFTimeInterval) {
        if running {
            let now = NSDate()
            
            if let unwrappedLastUpdate = lastUpdate {
                timeSurvived += now.timeIntervalSinceDate(unwrappedLastUpdate)
                timer?.text = "Time: \(round(timeSurvived * 10.0) / 10.0)s"
            }
            
            lastUpdate = now
        }
        
        for bar in bars {
            if bar.position.y >= self.frame.maxY {
                bar.removeFromParent()
            }
        }
        
        if let unwrappedPlayer = player {
            if (unwrappedPlayer.position.y - 15 >= self.frame.maxY) || (unwrappedPlayer.position.y <= self.frame.minY) {
                for bar in bars {
                    bar.removeFromParent()
                }
                
                self.removeActionForKey("barGeneration")
                bars.removeAll()
                player?.removeFromParent()
                player = nil
                running = false
                gameOver?.hidden = false
                gameOver?.text = "You died after \(round(timeSurvived * 10.0) / 10.0)s"
                status?.hidden = false
                status?.text = "TOUCH THE SCREEN TO RESTART"
            }
        }
    }
}
