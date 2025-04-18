import Phaser from "phaser"
import Button from "./uiObjs/Button"
import ProgressBar from "./uiObjs/progressBar"
import Icon from "./uiObjs/Icon"
// import Prompt from "./uiObjs/Prompt"
import Info from "./uiObjs/info"

/**
 * ui类
 * 封装了常用的ui组件
 */
export default class UI {
    static button(scene, x, y,  depth, info, callback){
        return new Button(scene, x, y, depth, info, callback)
    }
    static icon(scene, x, y, texture){
        return new Icon(scene, x, y, texture)
    }
    static info(obj, distanceX, distanceY){
        return new Info(obj, distanceX, distanceY)
    }
    static progressBar(scene, x, y){
        return new ProgressBar(scene, x, y)
    }
    // static prompt(scene, x, y, depth, info, children){
    //     return new Prompt(scene, x, y, depth, info, children)
    // }
    // static popUp(scene, x, y, depth, info, callback1, callback2){
    //     const popUp = UI.prompt(scene, x, y, depth, info).setScrollFactor(0)
    //     const cancellBtn = UI.button(scene, -200, 150, 10, "取消", function(){
    //         popUp.destroy()
    //         callback1()
    //     }).setScrollFactor(0)
    //     const sureBtn = UI.button(scene, 200, 150, 10, "确定", function(){
    //         popUp.destroy()
    //         callback2()
    //     }).setScrollFactor(0)
    //     cancellBtn.bg.setScrollFactor(0)
    //     sureBtn.bg.setScrollFactor(0)
    //     popUp.add([cancellBtn, sureBtn])
    //     return popUp
    // }
}