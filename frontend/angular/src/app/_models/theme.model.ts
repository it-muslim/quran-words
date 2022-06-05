export class Theme {
    fontsize = 2.5;
    bgcolor = '#eeeeee';
    color = '#272727';
    highlighted = '#64a367';
    shadowcolor = '#ffffff';
    shadowsize = 2;

    getShadow() {
        return `0px 0px ${this.shadowsize}px ${this.shadowcolor}`;
    }
    getFontSize() {
        return `${this.fontsize}rem`;
    }
}
