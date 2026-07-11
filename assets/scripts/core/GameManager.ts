/**
 * 还礼仙翁传 - 游戏状态与逻辑管理
 */
import {
    REALMS, LOCATIONS, STORY_EVENTS, CHARACTERS, LUCK_ENEMIES, EVENT_LUCK_ENEMY,
    LocationKey, ActionDef, GiftDef, StoryEvent,
    MONTHLY_GIFT_QUOTA, KARMA_DEBT_BURST_THRESHOLD,
    calcReturnMultiplier, getEndorsementBonus, ENDORSEMENT_TIERS, CRIT_BONUS_CAP,
    getDwellingDef, CAVE_ROOM_IDS, CaveRoomId,
    FormationId, FormationState, DanShiRank, PartnerSlot,
    buildInitialFormations, EVENT_FORMATION, EVENT_PARTNER,
    PARTNER_SLOT_MAX, DAN_SHI_RANK_LABEL, FORMATION_LABELS,
} from '../data/GameData';

export interface GameStateData {
    age: number;
    lifespan: number;
    realm: number;
    cultivation: number;
    karma: number;
    karmaDebt: number;
    spiritStones: number;
    giftQuota: number;
    currentLocation: LocationKey;
    cooldowns: Record<string, number>;
    completedOnce: string[];
    firstGifts: string[];
    triggeredEvents: string[];
    totalActions: number;
    gameWon: boolean;
    /** 气运之女羁绊度 characterId → 0-100 */
    bonds: Record<string, number>;
    /** 气运之敌击杀暴击叠层（上限 CRIT_BONUS_CAP） */
    critBonus: number;
    /** 已击杀气运之敌 ID */
    defeatedEnemies: string[];
    /** 洞府位阶 0～7，对应 D0～D7 */
    dwellingTier: number;
    /** 已解锁洞府功能区 */
    caveRoomsUnlocked: string[];
    /** 缘箓转数 0～9 */
    yuanZhuan: number;
    /** 阵法 Z01～Z12 状态 */
    formations: Record<FormationId, FormationState>;
    /** 苏念慈丹师品阶 */
    danShiRank: DanShiRank;
    /** 纳绶名册（正绶+侧绶） */
    partnerSlots: PartnerSlot[];
    /** D5 剧情解锁（合契丹→d5_unlock 事件确认后） */
    d5Unlocked: boolean;
}

export type LogCallback = (message: string, type?: string) => void;
export type EventCallback = (eventId: string, event: StoryEvent) => void;

const SAVE_KEY = 'elderCultivatorSave_v7';

function buildInitialBonds(): Record<string, number> {
    const bonds: Record<string, number> = {};
    for (const c of Object.values(CHARACTERS)) {
        if (c.luckRole === 'ally') bonds[c.id] = c.initialBond;
    }
    return bonds;
}

export class GameManager {
    private state: GameStateData;
    private onLog: LogCallback;
    private onEvent: EventCallback;
    private onStateChange: () => void;

    constructor(onLog: LogCallback, onEvent: EventCallback, onStateChange: () => void) {
        this.onLog = onLog;
        this.onEvent = onEvent;
        this.onStateChange = onStateChange;
        this.state = this.createInitialState();
    }

    private createInitialState(): GameStateData {
        return {
            age: 72,
            lifespan: 9,
            realm: 0,
            cultivation: 0,
            karma: 0,
            karmaDebt: 0,
            spiritStones: 0,
            giftQuota: MONTHLY_GIFT_QUOTA,
            currentLocation: 'gate',
            cooldowns: {},
            completedOnce: [],
            firstGifts: [],
            triggeredEvents: [],
            totalActions: 0,
            gameWon: false,
            bonds: buildInitialBonds(),
            critBonus: 0,
            defeatedEnemies: [],
            dwellingTier: 1,
            caveRoomsUnlocked: ['meditation'],
            yuanZhuan: 0,
            formations: buildInitialFormations(),
            danShiRank: 3,
            partnerSlots: [],
            d5Unlocked: false,
        };
    }

    getState(): Readonly<GameStateData> {
        return this.state;
    }

    getRealm() {
        return REALMS[this.state.realm] || REALMS[0];
    }

    loadSave(): boolean {
        const saved = localStorage.getItem(SAVE_KEY)
            ?? localStorage.getItem('elderCultivatorSave_v6')
            ?? localStorage.getItem('elderCultivatorSave_v5');
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                if (parsed.lifespan !== undefined) {
                    this.state = { ...this.createInitialState(), ...parsed };
                    if (!this.state.bonds || Object.keys(this.state.bonds).length === 0) {
                        this.state.bonds = buildInitialBonds();
                    }
                    if (this.state.critBonus === undefined) this.state.critBonus = 0;
                    if (!this.state.defeatedEnemies) this.state.defeatedEnemies = [];
                    if (this.state.dwellingTier === undefined) this.state.dwellingTier = 1;
                    if (!this.state.caveRoomsUnlocked) this.state.caveRoomsUnlocked = ['meditation'];
                    if (this.state.yuanZhuan === undefined) this.state.yuanZhuan = 0;
                    if (!this.state.formations) this.state.formations = buildInitialFormations();
                    if (this.state.danShiRank === undefined) this.state.danShiRank = 3;
                    if (!this.state.partnerSlots) this.state.partnerSlots = [];
                    if (this.state.d5Unlocked === undefined) {
                        this.state.d5Unlocked = this.state.dwellingTier >= 5;
                    }
                    this.onLog('读取存档成功。', 'important');
                    this.onStateChange();
                    return true;
                }
            } catch {
                return false;
            }
        }
        return false;
    }

    saveGame() {
        localStorage.setItem(SAVE_KEY, JSON.stringify(this.state));
        this.onLog('存档成功。', 'important');
    }

    autoSave() {
        localStorage.setItem(SAVE_KEY, JSON.stringify(this.state));
    }

    resetGame() {
        localStorage.removeItem(SAVE_KEY);
        this.state = this.createInitialState();
        this.onStateChange();
    }

    startNewGame() {
        if (!this.loadSave()) {
            setTimeout(() => this.triggerEvent('prologue'), 300);
        }
        this.onLog('游戏开始。小回赠即时，大回赠因果爆发。');
    }

    switchLocation(locationId: LocationKey) {
        const location = LOCATIONS[locationId];
        if (locationId === 'mansion' && !this.isMansionUnlocked()) {
            this.onLog('纳绶别院尚未落成，需完成合契丹剧情并确认 D5 解锁。');
            return;
        }
        if (this.state.realm < location.unlockRealm) {
            this.onLog(`需要达到「${REALMS[location.unlockRealm].name}」才能前往。`);
            return;
        }
        this.state.currentLocation = locationId;
        this.onLog(`前往${location.name}`);
        this.onStateChange();
        this.autoSave();
    }

    isMansionUnlocked(): boolean {
        return this.state.d5Unlocked && this.state.dwellingTier >= 5;
    }

    getDanShiLabel(): string {
        return DAN_SHI_RANK_LABEL[this.state.danShiRank];
    }

    getFormationSummary(): string {
        const active = (Object.keys(this.state.formations) as FormationId[])
            .filter(id => this.state.formations[id] === 'active')
            .map(id => id);
        return active.length ? `阵${active.join('/')}` : '阵—';
    }

    getPartnerSummary(): string {
        const n = this.state.partnerSlots.length;
        const primary = this.state.partnerSlots.filter(p => p.role === 'primary').length;
        return `纳绶${n}/${PARTNER_SLOT_MAX}(正${primary})`;
    }

    private activateFormation(id: FormationId) {
        if (this.state.formations[id] === 'spent') return;
        if (this.state.formations[id] !== 'active') {
            this.state.formations[id] = 'active';
            this.onLog(`【阵法】${FORMATION_LABELS[id]}（${id}）运转`, 'important');
        }
    }

    private addPartner(slot: PartnerSlot) {
        if (this.state.partnerSlots.length >= PARTNER_SLOT_MAX) {
            this.onLog('纳绶名册已满。');
            return;
        }
        if (this.state.partnerSlots.some(p => p.characterId === slot.characterId)) return;

        this.state.partnerSlots.push(slot);
        const character = CHARACTERS[slot.characterId];
        const roleLabel = slot.role === 'primary' ? '正绶' : '侧绶';
        this.onLog(`【纳绶】${character?.name ?? slot.characterId}·${roleLabel}入册`, 'important');
        this.addBond(slot.characterId, 10);
    }

    private applyPartnersFromEvent(eventId: string) {
        const entry = EVENT_PARTNER[eventId];
        if (!entry) return;
        const slots = Array.isArray(entry) ? entry : [entry];
        for (const slot of slots) this.addPartner(slot);
    }

    private applyD5Unlock() {
        if (this.state.dwellingTier >= 5 && this.state.d5Unlocked) return;

        this.state.d5Unlocked = true;
        this.state.dwellingTier = 5;
        this.state.yuanZhuan = Math.max(this.state.yuanZhuan, 8);
        for (const room of CAVE_ROOM_IDS) this.unlockCaveRoom(room);
        this.activateFormation('Z11');
        this.onLog('【洞府】纳绶别院落成，缘修+20%', 'important');
    }

    private tryOfferHezhaoDan() {
        if (this.state.triggeredEvents.includes('hezhao_dan')) return;
        if (!this.state.defeatedEnemies.includes('han_tieshan')) return;
        if (this.state.realm < 5 || this.state.karma < 50) return;

        this.state.triggeredEvents.push('hezhao_dan');
        this.triggerEvent('hezhao_dan');
    }

    private tryOfferD5Unlock() {
        if (this.state.d5Unlocked || this.state.dwellingTier >= 5) return;
        if (!this.state.triggeredEvents.includes('hezhao_dan')) return;
        if (this.state.realm < 6 || this.state.karma < 40) return;
        if (this.state.triggeredEvents.includes('d5_unlock_offered')) return;

        this.state.triggeredEvents.push('d5_unlock_offered');
        this.triggerEvent('d5_unlock');
    }

    getDwellingBonus(): number {
        return getDwellingDef(this.state.dwellingTier).yinXiuBonus;
    }

    getDwellingLabel(): string {
        const def = getDwellingDef(this.state.dwellingTier);
        return `${def.id}·${def.name}`;
    }

    private unlockCaveRoom(roomId: CaveRoomId) {
        if (!this.state.caveRoomsUnlocked.includes(roomId)) {
            this.state.caveRoomsUnlocked.push(roomId);
        }
    }

    private checkDwellingUpgrade() {
        if (this.state.dwellingTier < 2 && this.state.realm >= 2) {
            this.state.dwellingTier = 2;
            this.unlockCaveRoom('dan_room');
        }
        if (this.state.dwellingTier < 3 && this.state.realm >= 3) {
            this.state.dwellingTier = 3;
        }
        if (this.state.dwellingTier < 4 && this.state.yuanZhuan >= 8) {
            this.state.dwellingTier = 4;
        }
        this.tryOfferHezhaoDan();
        this.tryOfferD5Unlock();
        if (this.state.dwellingTier < 6 && this.state.realm >= 7) {
            this.state.dwellingTier = 6;
            this.state.yuanZhuan = 9;
            this.state.danShiRank = 8;
            this.onLog('【洞府】赠缘洞天开门，缘修+25%', 'important');
        }
        this.syncDanShiRank();
    }

    private syncDanShiRank() {
        const rankByRealm: Partial<Record<number, DanShiRank>> = {
            2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8,
        };
        const target = rankByRealm[this.state.realm];
        if (target && this.state.danShiRank < target) {
            this.state.danShiRank = target;
            this.onLog(`【丹道】苏念慈升至${DAN_SHI_RANK_LABEL[target]}`, 'important');
        }
    }

    canAfford(cost?: Partial<{ spiritStones: number; karma: number; giftQuota: number }>): boolean {
        if (!cost) return true;
        if (cost.spiritStones && this.state.spiritStones < cost.spiritStones) return false;
        if (cost.karma && this.state.karma < cost.karma) return false;
        if (cost.giftQuota && this.state.giftQuota < cost.giftQuota) return false;
        return true;
    }

    private applyReward(reward?: Partial<Record<string, number>>) {
        if (!reward) return;
        if (reward.karma) this.state.karma += reward.karma;
        if (reward.karmaDebt) this.state.karmaDebt += reward.karmaDebt;
        if (reward.cultivation) this.state.cultivation += reward.cultivation;
        if (reward.spiritStones) this.state.spiritStones = Math.max(0, this.state.spiritStones + reward.spiritStones);
        if (reward.lifespan) this.state.lifespan += reward.lifespan;
        if (reward.giftQuota) this.state.giftQuota += reward.giftQuota;
        if (reward.realm !== undefined) {
            this.state.realm = Math.max(0, Math.min(REALMS.length - 1, this.state.realm + reward.realm));
        }
    }

    private applyCost(cost?: Partial<{ spiritStones: number; karma: number; giftQuota: number }>): boolean {
        if (!cost) return true;
        if (!this.canAfford(cost)) return false;
        if (cost.spiritStones) this.state.spiritStones -= cost.spiritStones;
        if (cost.karma) this.state.karma -= cost.karma;
        if (cost.giftQuota) this.state.giftQuota -= cost.giftQuota;
        return true;
    }

    private calcGiftMultiplier(characterId: string): { multiplier: number; isFirst: boolean; bond: number } {
        const character = CHARACTERS[characterId];
        if (!character) return { multiplier: 1, isFirst: false, bond: 0 };

        const isFirst = !this.state.firstGifts.includes(characterId);
        const bond = this.state.bonds[characterId] ?? character.initialBond ?? 0;
        const multiplier = calcReturnMultiplier({
            luck: character.luck,
            firstGiftBonus: character.firstGiftBonus,
            isFirst,
            bond,
            critBonus: this.state.critBonus,
        });

        if (isFirst) this.state.firstGifts.push(characterId);
        return { multiplier, isFirst, bond };
    }

    /** 击杀气运之敌，叠暴击倍率 */
    defeatLuckEnemy(enemyId: string): boolean {
        const enemy = LUCK_ENEMIES[enemyId];
        if (!enemy || this.state.defeatedEnemies.includes(enemyId)) return false;

        this.state.defeatedEnemies.push(enemyId);
        const before = this.state.critBonus;
        this.state.critBonus = Math.min(CRIT_BONUS_CAP, before + enemy.critPerKill);
        this.onLog(
            `【气运之敌】斩杀${enemy.name}，暴击倍率 +${Math.round(enemy.critPerKill * 100)}%（累计 +${Math.round(this.state.critBonus * 100)}%）`,
            'important',
        );
        return true;
    }

    private addBond(characterId: string, delta: number) {
        const character = CHARACTERS[characterId];
        if (!character || character.luckRole !== 'ally') return;

        const before = this.state.bonds[characterId] ?? character.initialBond;
        const after = Math.min(100, Math.max(0, before + delta));
        this.state.bonds[characterId] = after;

        for (const tier of ENDORSEMENT_TIERS) {
            if (before < tier.minBond && after >= tier.minBond) {
                this.onLog(`【返还背书】${character.name}·${tier.name}（羁绊${after}）`, 'important');
                break;
            }
        }
    }

    private scaleInstantReturn(base: Partial<Record<string, number>>, multiplier: number): Partial<Record<string, number>> {
        const scale = multiplier / 5;
        const result: Partial<Record<string, number>> = {};
        if (base.cultivation) result.cultivation = Math.max(1, Math.floor(base.cultivation * scale));
        if (base.spiritStones) result.spiritStones = Math.max(1, Math.floor(base.spiritStones * scale));
        if (base.karma) result.karma = Math.max(1, Math.floor(base.karma * scale));
        if (base.lifespan) result.lifespan = Math.max(1, Math.floor(base.lifespan * scale));
        return result;
    }

    performGift(gift: GiftDef) {
        if (gift.cost && !this.applyCost(gift.cost)) {
            if (gift.cost.giftQuota && this.state.giftQuota < (gift.cost.giftQuota || 0)) {
                this.onLog('本月赠礼次数已尽，等待下月重置。');
            } else {
                this.onLog('资源不足，无法赠礼。');
            }
            return;
        }

        const character = CHARACTERS[gift.targetId];
        if (!character) return;

        const { multiplier, isFirst, bond } = this.calcGiftMultiplier(character.id);
        if (isFirst) {
            this.onLog(`【首赠·${character.luck}级气运】赠礼${character.name}，倍率×${multiplier.toFixed(1)}`, 'important');
        }

        const bondGain = isFirst ? 15 : 5;
        this.addBond(character.id, bondGain);

        const scaled = this.scaleInstantReturn(gift.instantReturn || {}, multiplier);
        this.applyReward(scaled);

        const endorseBurst = getEndorsementBonus(bond, true);
        const karmaGain = Math.floor((gift.karmaGain || 0) * multiplier / 5);
        const debtGain = Math.floor((gift.karmaDebtGain || 0) * multiplier / 5 * (1 + endorseBurst));
        this.state.karma += karmaGain;
        this.state.karmaDebt += debtGain;

        this.onLog(`赠「${gift.name}」小回赠${this.formatReward(scaled)}，因果+${debtGain}（待爆发）`);

        if (gift.cooldown) this.state.cooldowns[gift.id] = gift.cooldown;
        if (gift.once) this.state.completedOnce.push(gift.id);

        this.state.totalActions++;
        if (gift.event) this.triggerEvent(gift.event);
        this.afterAction();
    }

    performAction(action: ActionDef) {
        if (action.cost && !this.applyCost(action.cost)) {
            this.onLog('资源不足，无法执行。');
            return;
        }

        const reward = this.applyDwellingBonus(action.reward);
        this.applyReward(reward);
        this.onLog(`「${action.name}」${this.formatReward(reward)}`);

        if (action.cooldown) this.state.cooldowns[action.id] = action.cooldown;
        if (action.once) this.state.completedOnce.push(action.id);

        this.state.totalActions++;
        if (action.event) this.triggerEvent(action.event);
        this.afterAction();
    }

    /** 洞府缘修加成作用于闭关/别院日常 */
    private applyDwellingBonus(reward?: Partial<Record<string, number>>): Partial<Record<string, number>> | undefined {
        if (!reward?.cultivation) return reward;
        const bonus = this.getDwellingBonus();
        if (bonus <= 0) return reward;
        return {
            ...reward,
            cultivation: Math.max(1, Math.floor(reward.cultivation * (1 + bonus))),
        };
    }

    private afterAction() {
        this.checkRandomEvents();
        this.checkKarmaBurst();
        this.checkDwellingUpgrade();
        this.tickCooldowns();
        this.checkBreakthrough();
        this.checkMonthPass();
        this.onStateChange();
        this.autoSave();
    }

    private formatReward(reward?: Partial<Record<string, number>>): string {
        if (!reward) return '';
        const parts: string[] = [];
        if (reward.karma && reward.karma > 0) parts.push(`善缘+${reward.karma}`);
        if (reward.cultivation && reward.cultivation > 0) parts.push(`修为+${reward.cultivation}`);
        if (reward.spiritStones && reward.spiritStones > 0) parts.push(`灵石+${reward.spiritStones}`);
        if (reward.lifespan && reward.lifespan > 0) parts.push(`寿元+${reward.lifespan}月`);
        return parts.length ? `：${parts.join('、')}` : '';
    }

    private tickCooldowns() {
        for (const key of Object.keys(this.state.cooldowns)) {
            if (this.state.cooldowns[key] > 0) this.state.cooldowns[key]--;
        }
    }

    cultivate() {
        const realm = this.getRealm();
        if (this.state.cultivation < realm.maxCultivation) {
            this.onLog('修为未满，无法突破。继续赠礼积因果吧。');
            return;
        }

        const nextRealm = REALMS[this.state.realm + 1];
        if (!nextRealm) {
            if (this.state.realm >= 7 && !this.state.gameWon) {
                this.triggerEvent('ending');
                this.state.gameWon = true;
            } else {
                this.onLog('已达当前版本最高境界。');
            }
            return;
        }

        if (nextRealm.cost && !this.applyCost(nextRealm.cost)) {
            this.onLog(`突破${nextRealm.name}需要：灵石${nextRealm.cost.spiritStones}，善缘${nextRealm.cost.karma}`);
            return;
        }

        this.state.realm++;
        this.state.cultivation = 0;
        this.onLog(`【突破】恭喜突破至「${nextRealm.name}」！`, 'important');
        this.onStateChange();
        this.autoSave();
    }

    settleKarma() {
        if (this.state.karmaDebt < 20) {
            this.onLog('因果不足20，尚无法结算大回赠。');
            return;
        }

        const settle = Math.min(this.state.karmaDebt, 50);
        const burstMult = 1 + getEndorsementBonus(this.getMaxBond(), true) + Math.min(this.state.critBonus, CRIT_BONUS_CAP);
        const cultivationGain = Math.floor(settle * 1.5 * burstMult);
        const stoneGain = Math.floor(settle * 0.8 * burstMult);

        this.state.karmaDebt -= settle;
        this.state.cultivation += cultivationGain;
        this.state.spiritStones += stoneGain;

        this.onLog(`【因果大回赠】消耗因果${settle}，修为+${cultivationGain}，灵石+${stoneGain}`, 'important');
        this.onStateChange();
        this.autoSave();
    }

    private checkKarmaBurst() {
        if (this.state.karmaDebt >= KARMA_DEBT_BURST_THRESHOLD && !this.state.triggeredEvents.includes('karma_burst')) {
            this.triggerEvent('karma_burst');
            this.state.triggeredEvents.push('karma_burst');
            this.state.karmaDebt = Math.floor(this.state.karmaDebt / 2);
        }
    }

    private checkBreakthrough() {
        const realm = this.getRealm();
        if (this.state.cultivation >= realm.maxCultivation) {
            this.onLog('修为已满，可以尝试突破了！', 'important');
        }
    }

    private checkRandomEvents() {
        if (this.state.karma >= 20 && !this.state.triggeredEvents.includes('rumor_event')) {
            if (Math.random() < 0.25) {
                this.triggerEvent('rumor_event');
                this.state.triggeredEvents.push('rumor_event');
            }
        }
    }

    private checkMonthPass() {
        if (this.state.totalActions > 0 && this.state.totalActions % 15 === 0) {
            this.state.giftQuota = MONTHLY_GIFT_QUOTA;
            this.state.lifespan--;
            if (this.state.lifespan <= 0) {
                this.onLog('【寿元耗尽】莫长春坐化而去……', 'event');
                this.state.gameWon = false;
            } else {
                this.onLog(`一月过去，赠礼次数重置。寿元剩${this.state.lifespan}月。`);
            }
        }
    }

    triggerEvent(eventId: string) {
        const event = STORY_EVENTS[eventId];
        if (event) this.onEvent(eventId, event);
    }

    handleEventChoice(eventId: string, choiceIndex: number) {
        const event = STORY_EVENTS[eventId];
        if (!event) return;

        const choice = event.choices[choiceIndex];
        if (!choice) return;

        if (choice.cost && !this.applyCost(choice.cost)) {
            this.onLog('资源不足，无法选择此选项。');
            return;
        }

        this.applyReward(choice.effect);
        if (choice.log) this.onLog(choice.log, 'event');

        const enemyId = EVENT_LUCK_ENEMY[eventId];
        if (enemyId) this.defeatLuckEnemy(enemyId);

        const formationId = EVENT_FORMATION[eventId];
        if (formationId) this.activateFormation(formationId);

        if (eventId === 'd5_unlock') {
            this.applyD5Unlock();
            if (!this.state.triggeredEvents.includes('d5_unlock')) {
                this.state.triggeredEvents.push('d5_unlock');
            }
        }

        this.applyPartnersFromEvent(eventId);

        this.onStateChange();
        this.autoSave();
    }

    isGiftAvailable(gift: GiftDef): { available: boolean; reason?: string } {
        const onCooldown = (this.state.cooldowns[gift.id] || 0) > 0;
        const completed = gift.once && this.state.completedOnce.includes(gift.id);
        const cantAfford = gift.cost && !this.canAfford(gift.cost);

        if (completed) return { available: false, reason: '已赠过' };
        if (onCooldown) return { available: false, reason: `冷却${this.state.cooldowns[gift.id]}` };
        if (cantAfford) {
            if (gift.cost?.giftQuota && this.state.giftQuota < gift.cost.giftQuota) {
                return { available: false, reason: '赠礼次数不足' };
            }
            return { available: false, reason: '资源不足' };
        }
        return { available: true };
    }

    isActionAvailable(action: ActionDef): { available: boolean; reason?: string } {
        const onCooldown = (this.state.cooldowns[action.id] || 0) > 0;
        const completed = action.once && this.state.completedOnce.includes(action.id);
        const cantAfford = action.cost && !this.canAfford(action.cost);
        const realmLocked = action.unlockRealm !== undefined && this.state.realm < action.unlockRealm;

        if (completed) return { available: false, reason: '已完成' };
        if (realmLocked) return { available: false, reason: `需${REALMS[action.unlockRealm!].name}` };
        if (action.id === 'mansion_partner_liu' && !this.state.d5Unlocked) {
            return { available: false, reason: '需D5落成' };
        }
        if (action.id === 'mansion_partner_su' && !this.state.completedOnce.includes('mansion_partner_liu')) {
            return { available: false, reason: '需柳氏纳绶' };
        }
        if (onCooldown) return { available: false, reason: `冷却${this.state.cooldowns[action.id]}` };
        if (cantAfford) return { available: false, reason: '资源不足' };
        return { available: true };
    }

    private getMaxBond(): number {
        return Math.max(0, ...Object.values(this.state.bonds));
    }

    getCritBonus(): number {
        return this.state.critBonus;
    }

    isLocationUnlocked(locationId: LocationKey): boolean {
        if (locationId === 'mansion') return this.isMansionUnlocked() && this.state.realm >= LOCATIONS.mansion.unlockRealm;
        return this.state.realm >= LOCATIONS[locationId].unlockRealm;
    }
}
