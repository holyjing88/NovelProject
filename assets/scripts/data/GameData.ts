/**
 * 还礼仙翁传 - 游戏数据定义
 * The Returning Gift Sage
 */

export type LuckGrade = '丁' | '丙' | '乙' | '甲' | '天';
export type LuckRole = 'ally' | 'enemy';

/** 气运之女背书档位 — docs/还礼仙翁传/12-气运系统.md §3.2 */
export interface EndorsementTier {
    minBond: number;
    name: string;
    instantBonus: number;
    burstBonus: number;
}

export interface CharacterDef {
    id: string;
    name: string;
    title: string;
    luck: LuckGrade;
    luckRole: LuckRole;
    firstGiftBonus: number;
    initialBond: number;
    desc: string;
}

/** 气运之敌 — 击杀叠暴击倍率 */
export interface LuckEnemyDef {
    id: string;
    name: string;
    luck: LuckGrade;
    critPerKill: number;
    storyAnchor: string;
    note?: string;
}

export interface RealmDef {
    id: number;
    name: string;
    maxCultivation: number;
    icon: string;
    cost?: { spiritStones: number; karma: number };
}

export interface GiftDef {
    id: string;
    name: string;
    targetId: string;
    cost?: Partial<GameCost>;
    instantReturn?: Partial<GameReward>;
    karmaGain?: number;
    karmaDebtGain?: number;
    cooldown?: number;
    once?: boolean;
    event?: string;
}

export interface ActionDef {
    id: string;
    name: string;
    reward?: Partial<GameReward>;
    cost?: Partial<GameCost>;
    cooldown?: number;
    once?: boolean;
    event?: string;
    /** 最低境界（REALMS.id）方可执行 */
    unlockRealm?: number;
}

export interface LocationDef {
    name: string;
    desc: string;
    unlockRealm: number;
    gifts: GiftDef[];
    actions: ActionDef[];
}

export interface GameReward {
    karma: number;
    karmaDebt: number;
    cultivation: number;
    spiritStones: number;
    lifespan: number;
    realm: number;
    giftQuota: number;
}

export interface GameCost {
    spiritStones: number;
    karma: number;
    giftQuota: number;
}

export interface EventChoice {
    text: string;
    cost?: Partial<GameCost>;
    effect?: Partial<GameReward>;
    log?: string;
}

export interface StoryEvent {
    title: string;
    text: string;
    choices: EventChoice[];
}

export const LUCK_MULTIPLIER: Record<LuckGrade, number> = {
    '丁': 2,
    '丙': 3,
    '乙': 5,
    '甲': 8,
    '天': 10,
};

/** 气运之女返还背书档位 */
export const ENDORSEMENT_TIERS: EndorsementTier[] = [
    { minBond: 80, name: '命背书', instantBonus: 0.35, burstBonus: 0.40 },
    { minBond: 60, name: '深背书', instantBonus: 0.20, burstBonus: 0.25 },
    { minBond: 40, name: '初背书', instantBonus: 0.10, burstBonus: 0.15 },
];

export const CRIT_BONUS_CAP = 1.0;

export const LUCK_ENEMIES: Record<string, LuckEnemyDef> = {
    chiyan_vanguard: { id: 'chiyan_vanguard', name: '赤焰先锋队长', luck: '丙', critPerKill: 0.10, storyAnchor: '部二·夜袭' },
    qinglin_demon: { id: 'qinglin_demon', name: '青鳞妖君', luck: '乙', critPerKill: 0.15, storyAnchor: '部二·双BOSS' },
    han_tieshan: { id: 'han_tieshan', name: '韩铁山', luck: '甲', critPerKill: 0.20, storyAnchor: '部八·ch876', note: '战至死，禁自刎' },
    duoyuan_elder: { id: 'duoyuan_elder', name: '夺缘宗执事', luck: '丙', critPerKill: 0.12, storyAnchor: '部八·ch896' },
};

/** 羁绊档位 → 返还背书加成（小回赠用 instant，爆发用 burst） */
export function getEndorsementBonus(bond: number, forBurst = false): number {
    for (const tier of ENDORSEMENT_TIERS) {
        if (bond >= tier.minBond) {
            return forBurst ? tier.burstBonus : tier.instantBonus;
        }
    }
    return 0;
}

/** 完整回赠倍率 — 气运+首赠+羁绊+背书+气运之敌暴击 */
export function calcReturnMultiplier(opts: {
    luck: LuckGrade;
    firstGiftBonus: number;
    isFirst: boolean;
    bond: number;
    critBonus: number;
}): number {
    let mult = LUCK_MULTIPLIER[opts.luck];
    if (opts.isFirst) mult *= opts.firstGiftBonus / 3;
    mult *= 1 + opts.bond / 200;
    mult *= 1 + getEndorsementBonus(opts.bond, false);
    mult *= 1 + Math.min(opts.critBonus, CRIT_BONUS_CAP);
    return mult;
}

export const REALMS: RealmDef[] = [
    { id: 0, name: '筑基中期', maxCultivation: 100, icon: '🌱' },
    { id: 1, name: '筑基后期', maxCultivation: 200, icon: '🍃', cost: { spiritStones: 50, karma: 10 } },
    { id: 2, name: '金丹初期', maxCultivation: 400, icon: '🔮', cost: { spiritStones: 150, karma: 30 } },
    { id: 3, name: '金丹中期', maxCultivation: 800, icon: '💎', cost: { spiritStones: 300, karma: 60 } },
    { id: 4, name: '金丹后期', maxCultivation: 1500, icon: '✨', cost: { spiritStones: 600, karma: 100 } },
    { id: 5, name: '元婴初期', maxCultivation: 3000, icon: '👤', cost: { spiritStones: 1200, karma: 200 } },
    { id: 6, name: '元婴中期', maxCultivation: 6000, icon: '🌟', cost: { spiritStones: 2500, karma: 400 } },
    { id: 7, name: '化神初期', maxCultivation: 12000, icon: '☀️', cost: { spiritStones: 5000, karma: 800 } },
];

export const CHARACTERS: Record<string, CharacterDef> = {
    shenwanqing: { id: 'shenwanqing', name: '沈晚晴', title: '太上长老', luck: '天', luckRole: 'ally', firstGiftBonus: 10, initialBond: 60, desc: '闭关前的师父，赠你续命丹' },
    liuqingyuan: { id: 'liuqingyuan', name: '柳青鸢', title: '青岚门宗主', luck: '甲', luckRole: 'ally', firstGiftBonus: 8, initialBond: 55, desc: '青梅竹马的小师妹' },
    sunianCi: { id: 'sunianCi', name: '苏念慈', title: '丹堂首座', luck: '乙', luckRole: 'ally', firstGiftBonus: 5, initialBond: 45, desc: '暗恋你三十年的师姐' },
    guxiaoman: { id: 'guxiaoman', name: '顾小满', title: '杂役少女', luck: '丁', luckRole: 'ally', firstGiftBonus: 3, initialBond: 20, desc: '扫地杂役，隐藏气运' },
    qinshangyan: { id: 'qinshangyan', name: '秦商言', title: '百宝阁管事', luck: '乙', luckRole: 'ally', firstGiftBonus: 5, initialBond: 30, desc: '商会女修，消息灵通' },
    liwushang: { id: 'liwushang', name: '厉无殇', title: '赤焰谷少谷主', luck: '丙', luckRole: 'ally', firstGiftBonus: 4, initialBond: 5, desc: '嚣张魔道，可赠礼羞辱（反戈后升忠诚）' },
};

export const LOCATIONS: Record<string, LocationDef> = {
    gate: {
        name: '青岚门 · 执法堂',
        desc: '莫长春挂名执法堂。渡劫失败后，同门窃窃私语：这老头还能活几天？',
        unlockRealm: 0,
        gifts: [
            { id: 'gift_pill_master', name: '赠续命丹给师父', targetId: 'shenwanqing', cost: { giftQuota: 1 }, instantReturn: { spiritStones: 30, lifespan: 10, cultivation: 10 }, karmaGain: 15, karmaDebtGain: 30, once: true, event: 'first_gift_master' },
            { id: 'gift_sword_sister', name: '赠旧法剑给青鸢', targetId: 'liuqingyuan', cost: { spiritStones: 10, giftQuota: 1 }, instantReturn: { cultivation: 15, spiritStones: 10 }, karmaGain: 10, karmaDebtGain: 20, cooldown: 3, event: 'gift_qingyuan' },
            { id: 'gift_herb_su', name: '赠药渣给念慈', targetId: 'sunianCi', cost: { giftQuota: 1 }, instantReturn: { cultivation: 10, spiritStones: 12 }, karmaGain: 8, karmaDebtGain: 15, cooldown: 2, event: 'gift_su' },
        ],
        actions: [
            { id: 'meditate', name: '拄杖静坐', reward: { cultivation: 5 } },
            { id: 'gossip', name: '听弟子闲话', reward: { karma: 2 }, cooldown: 1 },
            { id: 'patrol', name: '执法堂巡视', reward: { cultivation: 8, karma: 3 }, cooldown: 2 },
        ],
    },
    hall: {
        name: '青岚门 · 杂役丹堂',
        desc: '丹堂药香弥漫，杂役堂人声嘈杂。赵玄机常在此处冷眼旁观。',
        unlockRealm: 0,
        gifts: [
            { id: 'gift_stone_gu', name: '赠半块灵石给小满', targetId: 'guxiaoman', cost: { spiritStones: 5, giftQuota: 1 }, instantReturn: { spiritStones: 8, cultivation: 5 }, karmaGain: 5, karmaDebtGain: 25, once: true, event: 'gift_gu' },
            { id: 'gift_danfang_su', name: '赠丹方残页给念慈', targetId: 'sunianCi', cost: { spiritStones: 20, giftQuota: 1 }, instantReturn: { cultivation: 20, spiritStones: 15 }, karmaGain: 12, karmaDebtGain: 40, cooldown: 5, event: 'gift_danfang' },
        ],
        actions: [
            { id: 'sort_herbs', name: '整理药渣', reward: { cultivation: 5, spiritStones: 5 } },
            { id: 'teach', name: '指点杂役', reward: { karma: 4, cultivation: 3 }, cooldown: 2 },
            { id: 'alchemy', name: '旁听炼丹', reward: { cultivation: 10 }, cooldown: 3 },
            { id: 'slay_qinglin', name: '斩青鳞妖君', reward: { cultivation: 40, karma: 15 }, cooldown: 10, once: true, unlockRealm: 2, event: 'defeat_qinglin_demon' },
        ],
    },
    outside: {
        name: '东脉 · 百宝阁',
        desc: '百宝阁往来修士络绎不绝，赤焰谷的威胁如影随形。',
        unlockRealm: 1,
        gifts: [
            { id: 'gift_tea_qin', name: '赠茶饼给商言', targetId: 'qinshangyan', cost: { spiritStones: 8, giftQuota: 1 }, instantReturn: { spiritStones: 25, karma: 3 }, karmaGain: 10, karmaDebtGain: 20, cooldown: 4, event: 'gift_qin' },
            { id: 'gift_handkerchief', name: '赠手帕给无殇', targetId: 'liwushang', cost: { giftQuota: 1 }, instantReturn: { cultivation: 12, karma: 8 }, karmaGain: 8, karmaDebtGain: 50, cooldown: 10, event: 'humiliate_li' },
        ],
        actions: [
            { id: 'trade', name: '坊市闲逛', reward: { spiritStones: 10 }, cooldown: 2 },
            { id: 'inquiry', name: '打探赤焰谷', reward: { karma: 5 }, cooldown: 3, event: 'chiyan_intel' },
            { id: 'guard', name: '东脉巡守', reward: { cultivation: 15, karma: 5 }, cooldown: 5 },
            { id: 'slay_vanguard', name: '斩赤焰先锋', reward: { cultivation: 25, karma: 10 }, cooldown: 8, once: true, event: 'defeat_chiyan_vanguard' },
        ],
    },
    alliance: {
        name: '九府盟会',
        desc: '各方势力齐聚，灵脉分配之争一触即发。魏无涯笑里藏刀。',
        unlockRealm: 3,
        gifts: [
            { id: 'gift_cake_wei', name: '赠糕点给魏无涯', targetId: 'liwushang', cost: { spiritStones: 15, giftQuota: 1 }, instantReturn: { spiritStones: 40, cultivation: 15 }, karmaGain: 15, karmaDebtGain: 60, once: true, event: 'alliance_cake' },
            { id: 'gift_jade_li', name: '赠玉佩给厉无殇', targetId: 'liwushang', cost: { spiritStones: 50, giftQuota: 1 }, instantReturn: { cultivation: 30, spiritStones: 25 }, karmaGain: 20, karmaDebtGain: 100, cooldown: 15, event: 'jade_strike' },
        ],
        actions: [
            { id: 'negotiate', name: '盟会周旋', reward: { karma: 10, cultivation: 20 }, cooldown: 5 },
            { id: 'observe', name: '旁观各方博弈', reward: { karma: 8 }, cooldown: 3 },
            { id: 'slay_duoyuan', name: '灭夺缘执事', reward: { cultivation: 50, karma: 20 }, cooldown: 12, once: true, unlockRealm: 4, event: 'defeat_duoyuan_elder' },
            { id: 'slay_han', name: '韩铁山同陨', reward: { cultivation: 80, karma: 30 }, cooldown: 15, once: true, unlockRealm: 5, event: 'defeat_han_tieshan' },
        ],
    },
    mansion: {
        name: '纳绶别院 · D5',
        desc: '会客亭、丹房、藏礼阁……再活五百年，先从分间吵起。缘修+20%。',
        unlockRealm: 6,
        gifts: [],
        actions: [
            { id: 'mansion_meditate', name: '闭关位缘修', reward: { cultivation: 18 }, cooldown: 1 },
            { id: 'mansion_reception', name: '会客亭敬茶', reward: { karma: 12, cultivation: 8 }, cooldown: 5, event: 'mansion_reception' },
            { id: 'mansion_dan', name: '丹房旁听', reward: { cultivation: 12 }, cooldown: 3 },
            { id: 'mansion_vault', name: '藏礼阁整理', reward: { karma: 6, spiritStones: 8 }, cooldown: 4 },
            { id: 'mansion_nourish', name: '赠灵石养阵', cost: { spiritStones: 20 }, reward: { karma: 8, cultivation: 5 }, cooldown: 6, event: 'nourish_z11' },
            { id: 'mansion_ceremony', name: '落成礼观礼', reward: { karma: 15, cultivation: 20 }, once: true, event: 'd5_ceremony' },
            { id: 'mansion_partner_liu', name: '柳氏纳绶夜', reward: { karma: 12 }, once: true, event: 'partner_liu', unlockRealm: 6 },
            { id: 'mansion_partner_su', name: '苏氏纳绶夜', reward: { karma: 12 }, once: true, event: 'partner_su', unlockRealm: 6 },
        ],
    },
};

/** 剧情事件 → 气运之敌 ID */
export const EVENT_LUCK_ENEMY: Record<string, string> = {
    defeat_chiyan_vanguard: 'chiyan_vanguard',
    defeat_qinglin_demon: 'qinglin_demon',
    defeat_duoyuan_elder: 'duoyuan_elder',
    defeat_han_tieshan: 'han_tieshan',
};

export const STORY_EVENTS: Record<string, StoryEvent> = {
    prologue: {
        title: '赠缘簿现世',
        text: '青岚峰上，沈晚晴闭关前召见你与柳青鸢。\n你上月渡劫失败，修为跌至筑基中期，寿元不足九月。\n沈晚晴赠续命丹：「再活五十年，找个伴，也不枉此生。」\n你接过丹药，心中暗喜：「终于有东西能送人了。」\n袖中一本泛黄簿册浮现——赠缘簿，小回赠即时，大回赠因果。',
        choices: [
            { text: '翻开赠缘簿，踏上赠礼修仙路', effect: { spiritStones: 30, giftQuota: 7 } },
        ],
    },
    first_gift_master: {
        title: '首赠师父',
        text: '你将师父所赐续命丹回赠沈晚晴。她愣住：「长春，这是为师给你的……」\n赠缘簿光芒大盛，首赠加成触发！即时小回赠已至，大因果正在累积……',
        choices: [
            { text: '「师父，弟子想让您安心闭关。」', effect: { cultivation: 50, spiritStones: 50 }, log: '天道返还青竹杖！此杖可随修为成长。' },
        ],
    },
    gift_qingyuan: {
        title: '赠剑青鸢',
        text: '你将旧法剑赠予柳青鸢。她抚剑不语，半晌道：「师兄，这剑跟了你两百年。」',
        choices: [
            { text: '「师兄老了，剑跟你有用。」', effect: { karma: 10 }, log: '柳青鸢收下青霜剑，小回赠剑意修为，因果已记。' },
            { text: '「青鸢，青岚门靠你了。」', effect: { karma: 15, cultivation: 20 }, log: '师妹重重点头，剑光一闪，天道回赠随之而来。' },
        ],
    },
    gift_su: {
        title: '赠药念慈',
        text: '苏念慈来送药，你反手将药渣赠她：「念慈，这渣里有灵气，别浪费。」\n她愣了愣，脸红道：「师兄……」',
        choices: [
            { text: '「别多想，炼丹用的。」', effect: { karma: 5 }, log: '苏念慈收下回春丹，赠缘簿即时记下一笔善缘。' },
            { text: '「念慈，师兄没几年了，这丹你留着。」', effect: { karma: 12, cultivation: 15 }, log: '师姐眼眶泛红，天道返还回春丹力。' },
        ],
    },
    gift_gu: {
        title: '赠石小满',
        text: '杂役堂角落，顾小满扫地时灵石落地。你捡起半块赠她：「拿着，买碗热粥。」\n赵玄机远处冷笑：「莫长老老不正经，勾搭杂役？」',
        choices: [
            { text: '不理流言', effect: { karma: 8 }, log: '流言四起，但顾小满深深鞠了一躬。' },
            { text: '当众斥赵玄机', effect: { karma: 15 }, log: '赵玄机面色铁青，弟子们窃窃私语。' },
        ],
    },
    gift_danfang: {
        title: '丹方残页',
        text: '你将珍藏的丹方残页赠予苏念慈。她震惊：「师兄，这是上古丹方！」',
        choices: [
            { text: '「丹堂需要你。」', effect: { cultivation: 40, karma: 10 }, log: '苏念慈突破在即，小回赠丹道感悟，因果已记。' },
        ],
    },
    gift_qin: {
        title: '茶饼换情报',
        text: '百宝阁中，秦商言打量你：「莫长老，风烛残年还来逛坊市？」\n你递上一盒茶饼：「商言，尝尝这茶。」',
        choices: [
            { text: '「顺便打听赤焰谷动向。」', effect: { spiritStones: 50, karma: 10 }, log: '秦商言低声透露：赤焰谷三月内必犯东脉。' },
            { text: '「老夫就想喝杯茶。」', effect: { karma: 5, spiritStones: 30 }, log: '商言莞尔，小回赠灵石，商会因果已记。' },
        ],
    },
    humiliate_li: {
        title: '手帕定身',
        text: '厉无殇当众嘲讽：「将死之人，也敢来东脉？」\n你不怒，掏出一方手帕：「少谷主，擦擦汗。」\n手帕中藏定身符，厉无殇当众僵住！即时回赠已至，因果仍在累积。',
        choices: [
            { text: '拄杖离去，笑而不语', effect: { karma: 20, cultivation: 30 }, log: '众人哗然，莫长春深藏不露？' },
        ],
    },
    chiyan_intel: {
        title: '赤焰谷逼近',
        text: '探子来报：赤焰谷要求青岚门让出东脉灵田，否则三月后兵临城下。',
        choices: [
            { text: '「急什么，礼还没送完呢。」', effect: { karma: 10 }, log: '你淡定饮茶，柳青鸢却急了。' },
            { text: '建议硬抗', effect: { karma: 15, cultivation: 20 }, log: '宗门长老分裂，主战主和争执不休。' },
        ],
    },
    rumor_event: {
        title: '流言四起',
        text: '弟子传言：「莫长老靠女人上位！」「千岁高龄，就是有心也无力啊！」',
        choices: [
            { text: '一笑置之', effect: { karma: 5 }, log: '你笑了笑：「他们说得对，老夫靠的就是这些人。」' },
            { text: '请宗主澄清', effect: { karma: 10 }, log: '柳青鸢当众维护师兄，流言稍歇。' },
        ],
    },
    karma_burst: {
        title: '因果大回赠',
        text: '赠缘簿上积压的因果善缘同时爆发，天道大回赠降临！',
        choices: [
            { text: '接受大回赠', effect: { cultivation: 100, spiritStones: 100 }, log: '青竹杖微颤，青霜剑长鸣，因果化修为！' },
        ],
    },
    alliance_cake: {
        title: '糕点藏密录',
        text: '九府盟会大殿，你赠魏无涯一盒糕点。他尝了一口，脸色骤变——糕中藏有盟会密录副本！',
        choices: [
            { text: '「魏主持，尝尝家乡味。」', effect: { karma: 25, spiritStones: 150 }, log: '魏无涯勾结赤焰谷的证据曝光！' },
        ],
    },
    jade_strike: {
        title: '玉佩化神一击',
        text: '厉无殇再度挑衅。你赠其一枚「普通」玉佩，因果善缘已满，玉佩爆发出惊天一击！',
        choices: [
            { text: '「够活到你后悔今天说的话。」', effect: { cultivation: 300, realm: 1 }, log: '厉无殇重伤退走，全场震惊！' },
        ],
    },
    defeat_chiyan_vanguard: {
        title: '气运之敌·赤焰先锋',
        text: '东脉夜战，赤焰先锋队长陨于阵前。赠缘簿一颤，收其气运——回赠暴击倍率永久提升。',
        choices: [
            { text: '「礼送出去了，该还回来了。」', log: '【气运之敌】击杀赤焰先锋' },
        ],
    },
    defeat_qinglin_demon: {
        title: '气运之敌·青鳞妖君',
        text: '东脉夜战第二线，青鳞妖君被杖剑斩落，妖核入手。簿上又添一笔气运——暴击再涨。',
        choices: [
            { text: '妖核赠苏，回赠加倍。', log: '【气运之敌】斩杀青鳞妖君' },
        ],
    },
    defeat_duoyuan_elder: {
        title: '气运之敌·夺缘执事',
        text: '护关阵外，夺缘宗执事形灭于金钟余波。邪修气运散入赠缘簿，回赠更狠。',
        choices: [
            { text: '「假缘收不得真礼。」', log: '【气运之敌】灭夺缘执事' },
        ],
    },
    defeat_han_tieshan: {
        title: '气运之敌·韩铁山',
        text: '东脉血战，韩铁山与赤焰长老同坠阵中——禁自刎，战至死。其甲级气运尽归簿，暴击叠至新高。',
        choices: [
            { text: '拄杖默立，不言胜败。', log: '【气运之敌】韩铁山同陨' },
        ],
    },
    ending: {
        title: '长生之赠',
        text: '赤焰谷退，沈晚晴渡劫成功。她见你从白发复黑：「长春，你还能活多久？」\n你拄杖大笑：「够活到把你们一个个嫁出去。」',
        choices: [
            { text: '「赠人一礼，天道还你十倍。」', effect: {}, log: '【真结局】还礼仙翁传，未完待续……' },
        ],
    },
    d5_unlock: {
        title: 'D5纳绶别院',
        text: '合契丹余温未散，别院三间正室四座偏厅终于定稿。匾上三字：纳绶别院。\n赠缘簿跳字：D5·预纳绶别院启。缘修加成+20%。',
        choices: [
            { text: '礼成了，人慢慢来。', effect: { karma: 10 }, log: '【洞府】D5纳绶别院解锁，Z11养阵可启。' },
        ],
    },
    d5_ceremony: {
        title: '落成礼',
        text: '霍镇山扛匾，霜雀为媒。柳青鸢举杯，四椅门外一排——莫长春坐门口，跟坐。\n灵石入Z11阵槽，养阵光微亮。',
        choices: [
            { text: '「别院今日起，开门纳客。」', effect: { karma: 12, cultivation: 15 }, log: '【洞府】D5落成礼成，会客亭请帖至。' },
        ],
    },
    mansion_reception: {
        title: '会客亭敬茶',
        text: '四女敬茶，座次无人肯让。莫长春在门外石阶坐定，不接茶，只道：「敬了就好。茶烫，慢喝。」',
        choices: [
            { text: '跟坐四椅', effect: { karma: 8 }, log: '会客亭眼神战两刻，胜在无人摔盏。' },
        ],
    },
    nourish_z11: {
        title: 'Z11养阵',
        text: '灵石入阵槽，别院门框嗡鸣。碑背隐隐呼应，像别院与赠缘碑本就是一脉。',
        choices: [
            { text: '继续养阵', effect: { karma: 5 }, log: 'Z11别院养阵运转中。' },
        ],
    },
    hezhao_dan: {
        title: '七品合契丹',
        text: '丹堂七品炉开，合契丹成。预纳绶窗口已至，别院分室图纸上，墨迹未干。\n赠缘簿跳字：可启D5纳绶别院。',
        choices: [
            { text: '「礼成了，别院挂牌。」', effect: { karma: 15, cultivation: 20 }, log: '【剧情】合契丹成·预纳绶窗口开启' },
        ],
    },
    partner_liu: {
        title: '纳绶·柳',
        text: '剑穗为媒，霜雀为证。柳青鸢正绶意向落定，侧碑柳氏名分与心名合一。',
        choices: [
            { text: '「青岚靠你们。」', effect: { karma: 10 }, log: '【纳绶】柳青鸢·正绶' },
        ],
    },
    partner_su: {
        title: '纳绶·苏',
        text: '丹心玉温，丹香为媒。苏念慈正绶意向落定；厉无殇山门请茶，侧绶意向入册。',
        choices: [
            { text: '「丹炉还开着。」', effect: { karma: 10 }, log: '【纳绶】苏念慈·正绶；厉无殇·侧绶意向' },
        ],
    },
};

export const LOCATION_KEYS = ['gate', 'hall', 'outside', 'alliance', 'mansion'] as const;
export type LocationKey = typeof LOCATION_KEYS[number];

export const MONTHLY_GIFT_QUOTA = 7;
export const KARMA_DEBT_BURST_THRESHOLD = 80;

/** 丹师品阶（苏念慈线）— docs/还礼仙翁传/11-阵法丹道系统.md §二 */
export type DanShiRank = 3 | 4 | 5 | 6 | 7 | 8 | 9;

/** 阵法 ID（Z 系）— docs/还礼仙翁传/11-阵法丹道系统.md §三 */
export type FormationId =
    | 'Z01' | 'Z02' | 'Z03' | 'Z04' | 'Z05' | 'Z06'
    | 'Z07' | 'Z08' | 'Z09' | 'Z10' | 'Z11' | 'Z12';

export type FormationState = 'locked' | 'active' | 'spent';

export const DAN_SHI_RANK_LABEL: Record<DanShiRank, string> = {
    3: '三品培元',
    4: '四品破障',
    5: '五品镇妖',
    6: '六品冢心',
    7: '七品盟誓',
    8: '八品长生',
    9: '九品天赐',
};

/** 洞府位阶 D0～D7 — docs/还礼仙翁传/08-道具灵宠洞府系统.md §4 */
export type CaveDwellingId = 'D0' | 'D1' | 'D2' | 'D3' | 'D4' | 'D5' | 'D6' | 'D7';

export interface CaveDwellingDef {
    id: CaveDwellingId;
    tier: number;
    name: string;
    yinXiuBonus: number;
    unlockHint: string;
}

export const CAVE_DWELLINGS: CaveDwellingDef[] = [
    { id: 'D0', tier: 0, name: '杂役通铺', yinXiuBonus: 0, unlockHint: '开局' },
    { id: 'D1', tier: 1, name: '莫长春小院', yinXiuBonus: 0.05, unlockHint: 'ch1' },
    { id: 'D2', tier: 2, name: '丹堂侧室', yinXiuBonus: 0.08, unlockHint: '苏赠礼#4' },
    { id: 'D3', tier: 3, name: '执法堂静室', yinXiuBonus: 0.10, unlockHint: '柳信任' },
    { id: 'D4', tier: 4, name: '枯荣泽别院', yinXiuBonus: 0.15, unlockHint: '缘箓八转' },
    { id: 'D5', tier: 5, name: '纳绶别院', yinXiuBonus: 0.20, unlockHint: 'ch898预纳绶' },
    { id: 'D6', tier: 6, name: '赠缘洞天', yinXiuBonus: 0.25, unlockHint: '化神稳固' },
    { id: 'D7', tier: 7, name: '上界别府', yinXiuBonus: 0.30, unlockHint: 'E14后' },
];

export const CAVE_ROOM_IDS = ['meditation', 'reception', 'dan_room', 'vault', 'nourish_array', 'pet_yard'] as const;
export type CaveRoomId = typeof CAVE_ROOM_IDS[number];

export const FORMATION_LABELS: Record<FormationId, string> = {
    Z01: '东脉灵阵盘',
    Z02: '青岚护山大阵',
    Z03: '丹堂地火阵',
    Z04: '纳绶同心阵',
    Z05: '沈师入关阵',
    Z06: '护关金钟阵',
    Z07: '赠缘塔幻阵',
    Z08: '万妖封印阵',
    Z09: '盟会座次阵',
    Z10: '秋拍护场阵',
    Z11: 'D5别院养阵',
    Z12: '升天雷劫阵',
};

export const FORMATION_IDS: FormationId[] = [
    'Z01', 'Z02', 'Z03', 'Z04', 'Z05', 'Z06',
    'Z07', 'Z08', 'Z09', 'Z10', 'Z11', 'Z12',
];

export type PartnerRole = 'primary' | 'side';

export interface PartnerSlot {
    characterId: string;
    role: PartnerRole;
}

export const PARTNER_SLOT_MAX = 4;

/** 剧情事件 → 阵法激活 */
export const EVENT_FORMATION: Partial<Record<string, FormationId>> = {
    defeat_qinglin_demon: 'Z03',
    defeat_duoyuan_elder: 'Z06',
    defeat_han_tieshan: 'Z06',
    hezhao_dan: 'Z04',
    d5_unlock: 'Z11',
    nourish_z11: 'Z11',
    d5_ceremony: 'Z04',
};

/** 剧情事件 → 纳绶入册 */
export const EVENT_PARTNER: Partial<Record<string, PartnerSlot | PartnerSlot[]>> = {
    partner_liu: { characterId: 'liuqingyuan', role: 'primary' },
    partner_su: [
        { characterId: 'sunianCi', role: 'primary' },
        { characterId: 'liwushang', role: 'side' },
    ],
};

export function buildInitialFormations(): Record<FormationId, FormationState> {
    const map = {} as Record<FormationId, FormationState>;
    for (const id of FORMATION_IDS) map[id] = 'locked';
    return map;
}

export function getDwellingDef(tier: number): CaveDwellingDef {
    return CAVE_DWELLINGS.find(d => d.tier === tier) ?? CAVE_DWELLINGS[1];
}
