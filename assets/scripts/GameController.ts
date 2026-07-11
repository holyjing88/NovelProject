/**
 * 还礼仙翁传 - 主界面控制器
 */
import { _decorator, Component, Node, Label, Button, Color, UITransform, Widget, Layout, Size, BlockInputEvents, Graphics } from 'cc';
import { GameManager } from './core/GameManager';
import { LOCATIONS, LocationKey, StoryEvent, ActionDef, GiftDef } from './data/GameData';

const { ccclass } = _decorator;

const COLORS = {
    bg: new Color(18, 28, 24, 255),
    panel: new Color(28, 42, 36, 255),
    card: new Color(38, 55, 46, 255),
    gold: new Color(200, 168, 90, 255),
    jade: new Color(90, 180, 140, 255),
    text: new Color(220, 230, 215, 255),
    textDim: new Color(140, 160, 145, 255),
    amber: new Color(220, 160, 60, 255),
};

@ccclass('GameController')
export class GameController extends Component {
    private gameManager!: GameManager;
    private uiRoot!: Node;

    private titleLabel!: Label;
    private subtitleLabel!: Label;
    private lifespanLabel!: Label;
    private realmLabel!: Label;
    private cultivationLabel!: Label;
    private karmaLabel!: Label;
    private karmaDebtLabel!: Label;
    private stonesLabel!: Label;
    private giftQuotaLabel!: Label;
    private locationNameLabel!: Label;
    private locationDescLabel!: Label;
    private logContent!: Node;
    private giftsContainer!: Node;
    private actionsContainer!: Node;
    private eventModal!: Node;
    private eventTitleLabel!: Label;
    private eventTextLabel!: Label;
    private eventChoicesContainer!: Node;
    private currentEventId = '';
    private mansionNavButton!: Node;

    start() {
        this.buildUI();
        this.initGame();
    }

    private initGame() {
        this.gameManager = new GameManager(
            (msg, type) => this.addLog(msg, type),
            (eventId, event) => this.showEvent(eventId, event),
            () => this.refreshUI(),
        );
        this.gameManager.startNewGame();
        this.refreshUI();
    }

    private buildUI() {
        const canvas = this.node.parent!;
        const canvasTransform = canvas.getComponent(UITransform)!;
        const W = canvasTransform.width;
        const H = canvasTransform.height;

        const bg = new Node('Background');
        bg.parent = canvas;
        bg.setSiblingIndex(0);
        const bgTransform = bg.addComponent(UITransform);
        bgTransform.setContentSize(W, H);
        const bgWidget = bg.addComponent(Widget);
        bgWidget.isAlignTop = bgWidget.isAlignBottom = bgWidget.isAlignLeft = bgWidget.isAlignRight = true;
        bgWidget.top = bgWidget.bottom = bgWidget.left = bgWidget.right = 0;
        const bgGfx = bg.addComponent(Graphics);
        bgGfx.fillColor = COLORS.bg;
        bgGfx.rect(-W / 2, -H / 2, W, H);
        bgGfx.fill();

        this.uiRoot = new Node('UIRoot');
        this.uiRoot.parent = canvas;
        const uiTransform = this.uiRoot.addComponent(UITransform);
        uiTransform.setContentSize(W, H);
        const uiWidget = this.uiRoot.addComponent(Widget);
        uiWidget.isAlignTop = uiWidget.isAlignBottom = uiWidget.isAlignLeft = uiWidget.isAlignRight = true;
        uiWidget.top = uiWidget.bottom = uiWidget.left = uiWidget.right = 0;

        const header = this.createPanel(this.uiRoot, 'Header', W - 40, 100, H / 2 - 60);
        this.titleLabel = this.createLabel(header, '还礼仙翁传', 36, COLORS.gold, 0, 20);
        this.subtitleLabel = this.createLabel(header, '小回赠即时，大回赠因果爆发', 20, COLORS.textDim, 0, -20);

        const statusPanel = this.createPanel(this.uiRoot, 'Status', W - 40, 220, H / 2 - 210);
        this.lifespanLabel = this.createLabel(statusPanel, '寿元: 9 月', 22, COLORS.amber, -200, 70);
        this.realmLabel = this.createLabel(statusPanel, '筑基中期', 22, COLORS.jade, 100, 70);
        this.cultivationLabel = this.createLabel(statusPanel, '修为: 0 / 100', 20, COLORS.text, -200, 30);
        this.karmaLabel = this.createLabel(statusPanel, '善缘: 0', 20, COLORS.jade, 100, 30);
        this.karmaDebtLabel = this.createLabel(statusPanel, '因果: 0', 20, COLORS.amber, -200, -10);
        this.stonesLabel = this.createLabel(statusPanel, '灵石: 0', 20, COLORS.gold, 100, -10);
        this.giftQuotaLabel = this.createLabel(statusPanel, '赠礼: 7/7', 17, COLORS.textDim, 0, -50);
        this.giftQuotaLabel.overflow = Label.Overflow.SHRINK;
        this.giftQuotaLabel.node.getComponent(UITransform)!.setContentSize(W - 60, 36);

        const locationPanel = this.createPanel(this.uiRoot, 'Location', W - 40, 90, H / 2 - 380);
        this.locationNameLabel = this.createLabel(locationPanel, '青岚门 · 执法堂', 24, COLORS.gold, 0, 18);
        this.locationDescLabel = this.createLabel(locationPanel, '', 17, COLORS.textDim, 0, -18);
        this.locationDescLabel.overflow = Label.Overflow.CLAMP;
        this.locationDescLabel.node.getComponent(UITransform)!.setContentSize(W - 80, 36);

        const giftsPanel = this.createPanel(this.uiRoot, 'Gifts', W - 40, 150, H / 2 - 490);
        this.createLabel(giftsPanel, '━━ 赠缘簿 ━━', 18, COLORS.jade, 0, 58);
        this.giftsContainer = new Node('GiftsList');
        this.giftsContainer.parent = giftsPanel;
        this.giftsContainer.setPosition(0, -10, 0);
        const giftsLayout = this.giftsContainer.addComponent(Layout);
        giftsLayout.type = Layout.Type.GRID;
        giftsLayout.resizeMode = Layout.ResizeMode.CONTAINER;
        giftsLayout.cellSize = new Size(150, 52);
        giftsLayout.spacingX = 8;
        giftsLayout.spacingY = 6;
        giftsLayout.constraintNum = 2;
        const giftsTransform = this.giftsContainer.addComponent(UITransform);
        giftsTransform.setContentSize(W - 60, 120);

        const actionsPanel = this.createPanel(this.uiRoot, 'Actions', W - 40, 130, 30);
        this.createLabel(actionsPanel, '━━ 日常 ━━', 18, COLORS.textDim, 0, 48);
        this.actionsContainer = new Node('ActionsList');
        this.actionsContainer.parent = actionsPanel;
        this.actionsContainer.setPosition(0, -8, 0);
        const actionsLayout = this.actionsContainer.addComponent(Layout);
        actionsLayout.type = Layout.Type.GRID;
        actionsLayout.resizeMode = Layout.ResizeMode.CONTAINER;
        actionsLayout.cellSize = new Size(150, 44);
        actionsLayout.spacingX = 8;
        actionsLayout.spacingY = 6;
        actionsLayout.constraintNum = 2;
        const actionsTransform = this.actionsContainer.addComponent(UITransform);
        actionsTransform.setContentSize(W - 60, 100);

        this.createButton(this.uiRoot, '🧘 闭关突破', -130, -H / 2 + 185, 180, 46, () => this.gameManager.cultivate());
        this.createButton(this.uiRoot, '⚡ 结算因果', 130, -H / 2 + 185, 180, 46, () => this.gameManager.settleKarma());

        const navY = -H / 2 + 115;
        const navKeys: { key: LocationKey; label: string }[] = [
            { key: 'gate', label: '🏛️ 执法堂' },
            { key: 'hall', label: '⚗️ 丹堂' },
            { key: 'outside', label: '🏪 百宝阁' },
            { key: 'alliance', label: '⚖️ 九府' },
        ];
        navKeys.forEach((nav, i) => {
            const x = -270 + i * 180;
            this.createButton(this.uiRoot, nav.label, x, navY, 160, 42, () => this.gameManager.switchLocation(nav.key));
        });

        this.mansionNavButton = this.createButton(this.uiRoot, '🏡 别院', 450, navY, 140, 42, () => this.gameManager.switchLocation('mansion')).node;
        this.mansionNavButton.active = false;

        const logPanel = this.createPanel(this.uiRoot, 'Log', W - 40, 150, -H / 2 + 255);
        this.createLabel(logPanel, '修仙志', 22, COLORS.gold, -250, 55);
        const logScroll = new Node('LogScroll');
        logScroll.parent = logPanel;
        const logScrollTransform = logScroll.addComponent(UITransform);
        logScrollTransform.setContentSize(W - 60, 110);
        logScroll.setPosition(0, -8, 0);
        this.logContent = new Node('LogContent');
        this.logContent.parent = logScroll;
        const logContentTransform = this.logContent.addComponent(UITransform);
        logContentTransform.setContentSize(W - 60, 110);
        const logLayout = this.logContent.addComponent(Layout);
        logLayout.type = Layout.Type.VERTICAL;
        logLayout.resizeMode = Layout.ResizeMode.CONTAINER;

        this.createButton(this.uiRoot, '存档', -280, -H / 2 + 50, 100, 36, () => this.gameManager.saveGame());
        this.createButton(this.uiRoot, '重开', 280, -H / 2 + 50, 100, 36, () => {
            this.gameManager.resetGame();
            this.gameManager.startNewGame();
            this.clearLogs();
            this.refreshUI();
        });

        this.buildEventModal(W, H);
    }

    private buildEventModal(W: number, H: number) {
        this.eventModal = new Node('EventModal');
        this.eventModal.parent = this.uiRoot;
        this.eventModal.active = false;
        const modalTransform = this.eventModal.addComponent(UITransform);
        modalTransform.setContentSize(W, H);
        const modalWidget = this.eventModal.addComponent(Widget);
        modalWidget.isAlignTop = modalWidget.isAlignBottom = modalWidget.isAlignLeft = modalWidget.isAlignRight = true;
        modalWidget.top = modalWidget.bottom = modalWidget.left = modalWidget.right = 0;
        this.eventModal.addComponent(BlockInputEvents);

        const overlay = new Node('Overlay');
        overlay.parent = this.eventModal;
        const overlayTransform = overlay.addComponent(UITransform);
        overlayTransform.setContentSize(W, H);
        const overlayGfx = overlay.addComponent(Graphics);
        overlayGfx.fillColor = new Color(0, 0, 0, 180);
        overlayGfx.rect(-W / 2, -H / 2, W, H);
        overlayGfx.fill();

        const dialog = this.createPanel(this.eventModal, 'Dialog', W - 80, 420, 0);
        this.eventTitleLabel = this.createLabel(dialog, '', 28, COLORS.gold, 0, 160);
        this.eventTextLabel = this.createLabel(dialog, '', 19, COLORS.text, 0, 40);
        this.eventTextLabel.overflow = Label.Overflow.RESIZE_HEIGHT;
        this.eventTextLabel.node.getComponent(UITransform)!.setContentSize(W - 120, 220);

        this.eventChoicesContainer = new Node('Choices');
        this.eventChoicesContainer.parent = dialog;
        this.eventChoicesContainer.setPosition(0, -110, 0);
        const choicesLayout = this.eventChoicesContainer.addComponent(Layout);
        choicesLayout.type = Layout.Type.VERTICAL;
        choicesLayout.spacingY = 8;
        choicesLayout.resizeMode = Layout.ResizeMode.CONTAINER;
        const choicesTransform = this.eventChoicesContainer.addComponent(UITransform);
        choicesTransform.setContentSize(W - 120, 200);
    }

    private createPanel(parent: Node, name: string, w: number, h: number, y: number): Node {
        const panel = new Node(name);
        panel.parent = parent;
        panel.setPosition(0, y, 0);
        const transform = panel.addComponent(UITransform);
        transform.setContentSize(w, h);
        const gfx = panel.addComponent(Graphics);
        gfx.fillColor = COLORS.panel;
        gfx.roundRect(-w / 2, -h / 2, w, h, 8);
        gfx.fill();
        gfx.strokeColor = new Color(60, 80, 65, 255);
        gfx.lineWidth = 1;
        gfx.roundRect(-w / 2, -h / 2, w, h, 8);
        gfx.stroke();
        return panel;
    }

    private createLabel(parent: Node, text: string, fontSize: number, color: Color, x: number, y: number): Label {
        const node = new Node('Label');
        node.parent = parent;
        node.setPosition(x, y, 0);
        const label = node.addComponent(Label);
        label.string = text;
        label.fontSize = fontSize;
        label.color = color;
        label.lineHeight = fontSize + 6;
        const transform = node.addComponent(UITransform);
        transform.setContentSize(300, fontSize + 10);
        return label;
    }

    private createButton(parent: Node, text: string, x: number, y: number, w: number, h: number, callback: () => void, accent = false): Button {
        const node = new Node('Button');
        node.parent = parent;
        node.setPosition(x, y, 0);
        const transform = node.addComponent(UITransform);
        transform.setContentSize(w, h);

        const gfx = node.addComponent(Graphics);
        gfx.fillColor = accent ? new Color(50, 70, 55, 255) : COLORS.card;
        gfx.roundRect(-w / 2, -h / 2, w, h, 6);
        gfx.fill();
        gfx.strokeColor = accent ? COLORS.jade : new Color(60, 80, 65, 255);
        gfx.lineWidth = 1;
        gfx.roundRect(-w / 2, -h / 2, w, h, 6);
        gfx.stroke();

        const labelNode = new Node('Label');
        labelNode.parent = node;
        const label = labelNode.addComponent(Label);
        label.string = text;
        label.fontSize = 16;
        label.color = accent ? COLORS.jade : COLORS.text;
        label.overflow = Label.Overflow.SHRINK;
        const labelTransform = labelNode.addComponent(UITransform);
        labelTransform.setContentSize(w - 8, h);

        const button = node.addComponent(Button);
        button.transition = Button.Transition.SCALE;
        button.zoomScale = 0.95;
        node.on(Button.EventType.CLICK, callback);
        return button;
    }

    private refreshUI() {
        const state = this.gameManager.getState();
        const realm = this.gameManager.getRealm();
        const location = LOCATIONS[state.currentLocation];

        this.lifespanLabel.string = `寿元: ${state.lifespan} 月`;
        this.realmLabel.string = `${realm.icon} ${realm.name}`;
        this.cultivationLabel.string = `修为: ${state.cultivation} / ${realm.maxCultivation}`;
        this.karmaLabel.string = `善缘: ${state.karma}`;
        this.karmaDebtLabel.string = `因果: ${state.karmaDebt}`;
        this.stonesLabel.string = `灵石: ${state.spiritStones}`;
        this.giftQuotaLabel.string = `赠礼${state.giftQuota}/7 · 暴击+${Math.round(this.gameManager.getCritBonus() * 100)}% · ${this.gameManager.getDwellingLabel()} · ${this.gameManager.getFormationSummary()} · ${this.gameManager.getPartnerSummary()} · ${this.gameManager.getDanShiLabel()}`;
        this.locationNameLabel.string = location.name;
        this.locationDescLabel.string = location.desc;

        if (this.mansionNavButton) {
            this.mansionNavButton.active = this.gameManager.isLocationUnlocked('mansion');
        }

        this.refreshGifts(location.gifts);
        this.refreshActions(location.actions);
    }

    private refreshGifts(gifts: GiftDef[]) {
        this.giftsContainer.removeAllChildren();
        gifts.forEach(gift => {
            const { available, reason } = this.gameManager.isGiftAvailable(gift);
            const displayText = available ? `🎁 ${gift.name}` : `${gift.name}\n(${reason})`;
            const btn = this.createButton(this.giftsContainer, displayText, 0, 0, 150, 52,
                () => { if (available) this.gameManager.performGift(gift); }, available);
            if (!available) {
                const label = btn.node.getComponentInChildren(Label);
                if (label) label.color = COLORS.textDim;
            }
        });
    }

    private refreshActions(actions: ActionDef[]) {
        this.actionsContainer.removeAllChildren();
        actions.forEach(action => {
            const { available, reason } = this.gameManager.isActionAvailable(action);
            const displayText = available ? action.name : `${action.name}\n(${reason})`;
            const btn = this.createButton(this.actionsContainer, displayText, 0, 0, 150, 44,
                () => { if (available) this.gameManager.performAction(action); });
            if (!available) {
                const label = btn.node.getComponentInChildren(Label);
                if (label) label.color = COLORS.textDim;
            }
        });
    }

    private addLog(message: string, type = '') {
        const entry = new Node('LogEntry');
        entry.parent = this.logContent;
        const label = entry.addComponent(Label);
        label.string = message;
        label.fontSize = 15;
        label.lineHeight = 20;
        label.color = type === 'important' ? COLORS.gold : type === 'event' ? COLORS.jade : COLORS.textDim;
        label.overflow = Label.Overflow.RESIZE_HEIGHT;
        const transform = entry.addComponent(UITransform);
        transform.setContentSize(600, 20);

        while (this.logContent.children.length > 30) {
            this.logContent.children[this.logContent.children.length - 1].destroy();
        }
    }

    private clearLogs() {
        this.logContent.removeAllChildren();
    }

    private showEvent(eventId: string, event: StoryEvent) {
        this.currentEventId = eventId;
        this.eventTitleLabel.string = event.title;
        this.eventTextLabel.string = event.text;
        this.eventChoicesContainer.removeAllChildren();

        event.choices.forEach((choice, index) => {
            let text = choice.text;
            if (choice.cost) {
                const parts: string[] = [];
                if (choice.cost.spiritStones) parts.push(`灵石-${choice.cost.spiritStones}`);
                if (choice.cost.karma) parts.push(`善缘-${choice.cost.karma}`);
                if (parts.length) text += `\n(消耗: ${parts.join('、')})`;
            }
            this.createButton(this.eventChoicesContainer, text, 0, 0, 500, 48,
                () => {
                    this.gameManager.handleEventChoice(this.currentEventId, index);
                    this.eventModal.active = false;
                }, true);
        });

        this.eventModal.active = true;
    }
}
