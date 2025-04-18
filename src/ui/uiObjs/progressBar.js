import Phaser from "phaser"

export default class ProgressBar extends Phaser.GameObjects.Container{
    constructor(scene, x, y){
        super(scene, x ,y)
        this.scene.add.existing(this)
        this.bgBar = this.scene.add.image(0, 0, "progressBar", 0).setOrigin(0).setDepth(0)
        this.progressBar = this.scene.add.image(0, 0, "progressBar", 1).setOrigin(0).setDepth(1)
        this.width = this.bgBar.width
        this.height = this.bgBar.height
        this.add(this.bgBar)
        this.add(this.progressBar)
        this.progressBar.setCrop(0, 0, 0, this.progressBar.height)
    }
    update(progress){
        this.progressBar.setCrop(0, 0, progress*this.progressBar.width, this.progressBar.height)
    }
}