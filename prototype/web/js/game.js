/**
 * 万古守灯人 - 游戏核心逻辑
 * Legend of the Elder Cultivator
 * 原创版权 · 独立创作
 */

// ========== 游戏数据 ==========

const REALMS = [
  { id: 0, name: '凡人', maxCultivation: 100, icon: '🪔' },
  { id: 1, name: '微光', maxCultivation: 200, icon: '✨', cost: { lampOil: 1, memories: 1 } },
  { id: 2, name: '烛火', maxCultivation: 400, icon: '🕯️', cost: { lampOil: 5, memories: 2 } },
  { id: 3, name: '灯芯', maxCultivation: 800, icon: '🔥', cost: { lampOil: 15, memories: 5 } },
  { id: 4, name: '灯盏', maxCultivation: 1500, icon: '🏮', cost: { lampOil: 40, memories: 10 } },
  { id: 5, name: '灯影', maxCultivation: 3000, icon: '👤', cost: { lampOil: 100, memories: 20 } },
  { id: 6, name: '灯骨', maxCultivation: 6000, icon: '💀', cost: { lampOil: 250, memories: 50 } },
  { id: 7, name: '灯魂', maxCultivation: 12000, icon: '👁️', cost: { lampOil: 600, memories: 100 } },
];

const LOCATIONS = {
  home: {
    name: '青萝镇 · 顾宅',
    desc: '江南水乡的青萝镇，顾迟年的老屋。镇口有一盏长明灯，风雨不灭。',
    unlockRealm: 0,
    actions: [
      { id: 'write_letter', name: '代写书信', reward: { humanWarmth: 2 }, cooldown: 0 },
      { id: 'copy_book', name: '誊抄账册', reward: { humanWarmth: 3 }, cooldown: 0 },
      { id: 'help_neighbor', name: '帮邻人办事', reward: { humanWarmth: 5 }, cooldown: 2 },
      { id: 'tend_lamp', name: '照料镇口长明灯', reward: { humanWarmth: 8, cultivation: 5 }, cooldown: 5 },
      { id: 'visit_pharmacy', name: '拜访沈氏药铺', reward: { humanWarmth: 4 }, cooldown: 3, event: 'meet_shenqinghe' },
    ],
  },
  sect: {
    name: '云岚宗 · 杂役堂',
    desc: '西南修仙大宗，顾迟年以六十岁高龄成为史上最老杂役弟子。',
    unlockRealm: 1,
    actions: [
      { id: 'carry_water', name: '挑水', reward: { humanWarmth: 2, cultivation: 3 }, cooldown: 0 },
      { id: 'clean_beast', name: '清理灵兽栏', reward: { humanWarmth: 3, cultivation: 5 }, cooldown: 1 },
      { id: 'sort_herbs', name: '整理药渣', reward: { humanWarmth: 4, cultivation: 8, lampOil: 1 }, cooldown: 3 },
      { id: 'night_watch', name: '黑风林守灯', reward: { cultivation: 20, memories: -1 }, cooldown: 10, event: 'blackwind_forest' },
      { id: 'library', name: '藏经阁听道', reward: { cultivation: 15 }, cooldown: 5, event: 'yunzhao_teaching' },
    ],
  },
  market: {
    name: '幽灯集',
    desc: '每月朔日子时开启的地下集市，以灯为契、以记忆为价。摊主裴无妄神秘莫测。',
    unlockRealm: 2,
    actions: [
      { id: 'buy_danfang', name: '购买疏脉丹方', cost: { lampOil: 3, memories: 2 }, reward: { cultivation: 50 }, cooldown: 0, once: true },
      { id: 'sell_herbs', name: '倒卖灵药', reward: { lampOil: 2, humanWarmth: 3 }, cooldown: 4 },
      { id: 'gamble', name: '灯油博弈', cost: { lampOil: 1 }, reward: { lampOil: 3 }, failReward: { lampOil: -1 }, cooldown: 2, chance: 0.5 },
      { id: 'trade_memory', name: '记忆换灯油', cost: { memories: 3 }, reward: { lampOil: 5 }, cooldown: 8 },
      { id: 'meet_pei', name: '拜访裴无妄', reward: {}, cooldown: 20, event: 'pei_wuwang' },
    ],
  },
  ridge: {
    name: '枯骨岭',
    desc: '南疆禁地，上古战场遗址。时间流速异常，一日如一年。',
    unlockRealm: 3,
    actions: [
      { id: 'meditate', name: '时间苦修', reward: { cultivation: 100 }, cooldown: 15 },
      { id: 'explore', name: '探索遗迹', reward: { cultivation: 50, memories: -2 }, cooldown: 10, event: 'time_shadow' },
      { id: 'gather_bone', name: '采集骨灵草', reward: { lampOil: 3, cultivation: 30 }, cooldown: 6 },
      { id: 'lamp_tomb', name: '万灯冢试炼', cost: { memories: 10, lampOil: 50 }, reward: { cultivation: 500 }, cooldown: 30, event: 'lamp_tomb' },
    ],
  },
};

const STORY_EVENTS = {
  prologue: {
    title: '守岁灯现世',
    text: '承平三十七年秋，顾迟年六十大寿。整理阁楼时发现一本无字书册，午夜自燃，浮现《守灯经》三字。书册燃尽，留下一盏青铜小灯——守岁灯。',
    choices: [
      { text: '拾起守岁灯，开始守灯之路', effect: { realm: 0, lampOil: 3 } },
    ],
  },
  meet_shenqinghe: {
    title: '沈氏药铺',
    text: '药铺掌柜沈青禾二十七岁，丈夫三年前死于豪强逼债。她认出了顾迟年——当年她母亲常提起的那个落第书生。',
    choices: [
      { text: '「青禾，有什么难处尽管说。」', effect: { humanWarmth: 10 }, log: '沈青禾感激地点头，你们的情谊更深了。' },
      { text: '「只是路过，随便看看。」', effect: { humanWarmth: 2 }, log: '沈青禾微微一笑，没有多问。' },
    ],
  },
  blackwind_forest: {
    title: '黑风林守灯',
    text: '选拔试炼：在黑风林中独守一夜灯火。林中迷雾重重，有迷路猎户的呼救声传来……',
    choices: [
      { text: '守好灯火，不为外事所动', effect: { cultivation: 30 }, log: '你坚守一夜，灯火未灭，通过了试炼。' },
      { text: '以微光指路，救下迷路猎户', effect: { cultivation: 20, humanWarmth: 15, realm: 1 }, log: '你用微光阶力量为猎户指路，云照长老暗中点头。' },
    ],
  },
  yunzhao_teaching: {
    title: '云照长老的教诲',
    text: '藏经阁中，守阁人云照长老放下书卷：「你这盏灯，不是为自己点的。」',
    choices: [
      { text: '「长老此言何意？」', effect: { cultivation: 30 }, log: '云照长老不再多言，但你心中若有所悟。' },
      { text: '默默行礼，继续扫地', effect: { humanWarmth: 5, cultivation: 20 }, log: '云照长老看着你，眼中闪过一丝赞许。' },
    ],
  },
  debt_crisis: {
    title: '豪强逼债',
    text: '青萝镇豪强带人围住沈氏药铺，拿出伪造借据，要青禾抵债为奴。镇口长明灯在风中摇曳……',
    choices: [
      { text: '以微光感知识破伪造借据', cost: { lampOil: 2 }, effect: { humanWarmth: 20, cultivation: 50 }, log: '借据上的墨迹新旧不一，豪强心虚而退。' },
      { text: '召集乡邻，以理力争', effect: { humanWarmth: 10 }, log: '乡亲们纷纷站出来，豪强暂时退去。' },
      { text: '忍气吞声，以后再想办法', effect: { humanWarmth: -5 }, log: '青禾眼中闪过失望，你心中愧疚。' },
    ],
  },
  pei_wuwang: {
    title: '裴无妄的摊位',
    text: '幽灯集深处，神秘摊主裴无妄摆出一排小瓶：「后悔药、忘情烛、续命油，客官要什么？」',
    choices: [
      { text: '「续命油怎么卖？」', cost: { memories: 5 }, effect: { lampOil: 10 }, log: '裴无妄收走你一段少年记忆，递来十滴灯油。' },
      { text: '「我不买后悔药。」', effect: { cultivation: 30 }, log: '裴无妄笑了：「有意思，不修改过去的人，越来越少了。」' },
      { text: '转身离开', effect: {}, log: '裴无妄的声音从身后传来：「你会回来的。」' },
    ],
  },
  time_shadow: {
    title: '时间残影',
    text: '枯骨岭中，你看见一个平行世界的自己——少年修仙，飞升瑶台。但那个世界的青萝镇，无人守灯，全镇覆灭于乱世。',
    choices: [
      { text: '「瑶台太冷，我这盏灯得在镇上亮。」', effect: { cultivation: 100, memories: -3 }, log: '你拒绝了交换，平行世界的幻影消散。' },
      { text: '伸出手，想要交换人生', effect: { realm: -3 }, log: '【坏结局】你遗忘了守灯的意义，神魂错乱……' },
    ],
  },
  lamp_tomb: {
    title: '万灯冢试炼',
    text: '万灯冢入口，需以真心记忆为祭。陆承安已先一步闯入，献祭他人记忆，神魂开始错乱。',
    choices: [
      { text: '献祭初恋记忆，踏入万灯冢', cost: { memories: 10 }, effect: { cultivation: 500, realm: 1, lampOil: 20 }, log: '你忘了初恋的模样，但获得了守岁灯第二块碎片。' },
      { text: '拉住陆承安：「你的灯，还没灭呢。」', effect: { humanWarmth: 30, cultivation: 200 }, log: '陆承安眼中恢复清明，低声道：「多谢。」' },
    ],
  },
  ending: {
    title: '万古长明',
    text: '天魔退散，雨过天晴。顾迟年站在镇口，守岁灯与长明灯融为一体。裴无妄问：「飞升之门已开，你走不走？」',
    choices: [
      { text: '「我走了，谁给赶夜路的人照路？」', effect: {}, log: '【真结局】你化作灯火融入长明灯，从此青萝镇风雨不灭。' },
    ],
  },
};

// ========== 游戏状态 ==========

let gameState = {
  age: 60,
  realm: 0,
  cultivation: 0,
  lampOil: 0,
  humanWarmth: 0,
  memories: 10,
  currentLocation: 'home',
  cooldowns: {},
  completedOnce: [],
  triggeredEvents: [],
  storyFlags: {},
  totalActions: 0,
  gameWon: false,
};

// ========== DOM 元素 ==========

const elements = {
  age: document.getElementById('age'),
  realm: document.getElementById('realm'),
  cultivationBar: document.getElementById('cultivationBar'),
  cultivationText: document.getElementById('cultivationText'),
  lampOil: document.getElementById('lampOil'),
  humanWarmth: document.getElementById('humanWarmth'),
  memories: document.getElementById('memories'),
  locationName: document.getElementById('locationName'),
  locationDesc: document.getElementById('locationDesc'),
  actions: document.getElementById('actions'),
  logContent: document.getElementById('logContent'),
  cultivateBtn: document.getElementById('cultivateBtn'),
  convertBtn: document.getElementById('convertBtn'),
  eventModal: document.getElementById('eventModal'),
  eventTitle: document.getElementById('eventTitle'),
  eventText: document.getElementById('eventText'),
  eventChoices: document.getElementById('eventChoices'),
  lampIcon: document.getElementById('lampIcon'),
  saveBtn: document.getElementById('saveBtn'),
  resetBtn: document.getElementById('resetBtn'),
};

// ========== 核心函数 ==========

function getCurrentRealm() {
  return REALMS[gameState.realm] || REALMS[0];
}

function addLog(message, type = '') {
  const entry = document.createElement('p');
  entry.className = `log-entry ${type}`;
  entry.textContent = message;
  elements.logContent.insertBefore(entry, elements.logContent.firstChild);
  if (elements.logContent.children.length > 50) {
    elements.logContent.removeChild(elements.logContent.lastChild);
  }
}

function updateUI() {
  const realm = getCurrentRealm();
  elements.age.textContent = gameState.age;
  elements.realm.textContent = realm.name;
  elements.lampOil.textContent = gameState.lampOil;
  elements.humanWarmth.textContent = gameState.humanWarmth;
  elements.memories.textContent = gameState.memories;
  elements.lampIcon.textContent = realm.icon;

  const progress = (gameState.cultivation / realm.maxCultivation) * 100;
  elements.cultivationBar.style.width = `${Math.min(progress, 100)}%`;
  elements.cultivationText.textContent = `${gameState.cultivation} / ${realm.maxCultivation}`;

  const location = LOCATIONS[gameState.currentLocation];
  elements.locationName.textContent = location.name;
  elements.locationDesc.textContent = location.desc;

  renderActions();
  updateNavButtons();
}

function renderActions() {
  const location = LOCATIONS[gameState.currentLocation];
  elements.actions.innerHTML = '';

  location.actions.forEach(action => {
    const btn = document.createElement('button');
    btn.className = 'btn btn-action';

    const onCooldown = gameState.cooldowns[action.id] > 0;
    const completed = action.once && gameState.completedOnce.includes(action.id);
    const cantAfford = action.cost && !canAfford(action.cost);

    let rewardText = '';
    if (action.reward) {
      const parts = [];
      if (action.reward.humanWarmth) parts.push(`烟火+${action.reward.humanWarmth}`);
      if (action.reward.cultivation) parts.push(`修为+${action.reward.cultivation}`);
      if (action.reward.lampOil) parts.push(`灯油+${action.reward.lampOil}`);
      rewardText = parts.join(' · ');
    }
    if (action.cost) {
      const parts = [];
      if (action.cost.lampOil) parts.push(`灯油-${action.cost.lampOil}`);
      if (action.cost.memories) parts.push(`记忆-${action.cost.memories}`);
      rewardText = parts.join(' · ');
    }

    btn.innerHTML = `
      <span class="action-name">${action.name}</span>
      <span class="action-reward">${rewardText || '触发事件'}</span>
    `;

    btn.disabled = onCooldown || completed || cantAfford;
    if (onCooldown) {
      btn.querySelector('.action-reward').textContent += ` (冷却${gameState.cooldowns[action.id]}回合)`;
    }
    if (completed) {
      btn.querySelector('.action-reward').textContent = '已完成';
    }

    btn.onclick = () => performAction(action);
    elements.actions.appendChild(btn);
  });
}

function canAfford(cost) {
  if (!cost) return true;
  if (cost.lampOil && gameState.lampOil < cost.lampOil) return false;
  if (cost.memories && gameState.memories < cost.memories) return false;
  return true;
}

function applyReward(reward) {
  if (!reward) return;
  if (reward.humanWarmth) gameState.humanWarmth += reward.humanWarmth;
  if (reward.cultivation) gameState.cultivation += reward.cultivation;
  if (reward.lampOil) gameState.lampOil = Math.max(0, gameState.lampOil + reward.lampOil);
  if (reward.memories) gameState.memories = Math.max(0, gameState.memories + reward.memories);
  if (reward.realm) gameState.realm = Math.max(0, Math.min(REALMS.length - 1, gameState.realm + reward.realm));
}

function applyCost(cost) {
  if (!cost) return true;
  if (!canAfford(cost)) return false;
  if (cost.lampOil) gameState.lampOil -= cost.lampOil;
  if (cost.memories) gameState.memories -= cost.memories;
  return true;
}

function performAction(action) {
  if (action.cost && !applyCost(action.cost)) {
    addLog('资源不足，无法执行此行动。');
    return;
  }

  // 概率失败
  if (action.chance && Math.random() > action.chance) {
    applyReward(action.failReward || {});
    addLog(`${action.name}失败了……`);
  } else {
    applyReward(action.reward);
    addLog(`完成「${action.name}」${formatReward(action.reward)}`);
  }

  if (action.cooldown) {
    gameState.cooldowns[action.id] = action.cooldown;
  }
  if (action.once) {
    gameState.completedOnce.push(action.id);
  }

  gameState.totalActions++;

  // 触发剧情事件
  if (action.event) {
    triggerEvent(action.event);
  }

  // 随机剧情触发
  checkRandomEvents();

  // 减少冷却
  tickCooldowns();

  // 检查突破
  checkBreakthrough();

  updateUI();
  autoSave();
}

function formatReward(reward) {
  if (!reward) return '';
  const parts = [];
  if (reward.humanWarmth > 0) parts.push(`烟火+${reward.humanWarmth}`);
  if (reward.cultivation > 0) parts.push(`修为+${reward.cultivation}`);
  if (reward.lampOil > 0) parts.push(`灯油+${reward.lampOil}`);
  return parts.length ? `，获得${parts.join('、')}` : '';
}

function tickCooldowns() {
  Object.keys(gameState.cooldowns).forEach(key => {
    if (gameState.cooldowns[key] > 0) {
      gameState.cooldowns[key]--;
    }
  });
}

function cultivate() {
  const realm = getCurrentRealm();
  if (gameState.cultivation < realm.maxCultivation) {
    addLog('修为未满，无法突破。继续积累吧。');
    return;
  }

  const nextRealm = REALMS[gameState.realm + 1];
  if (!nextRealm) {
    if (gameState.realm >= 7 && !gameState.gameWon) {
      triggerEvent('ending');
      gameState.gameWon = true;
    } else {
      addLog('已达当前版本最高境界。更多内容敬请期待……');
    }
    return;
  }

  if (nextRealm.cost) {
    if (!canAfford(nextRealm.cost)) {
      addLog(`突破${nextRealm.name}需要：灯油${nextRealm.cost.lampOil}滴，记忆${nextRealm.cost.memories}片`);
      return;
    }
    applyCost(nextRealm.cost);
  }

  gameState.realm++;
  gameState.cultivation = 0;
  addLog(`【突破】恭喜突破至「${nextRealm.name}」阶！`, 'important');
  updateUI();
  autoSave();
}

function convertWarmth() {
  if (gameState.humanWarmth < 10) {
    addLog('人间烟火不足10点，无法凝练灯油。');
    return;
  }
  const amount = Math.floor(gameState.humanWarmth / 10);
  gameState.humanWarmth -= amount * 10;
  gameState.lampOil += amount;
  addLog(`凝练${amount}滴灯油。`, 'important');
  updateUI();
  autoSave();
}

function checkBreakthrough() {
  const realm = getCurrentRealm();
  if (gameState.cultivation >= realm.maxCultivation) {
    addLog('修为已满，可以尝试突破了！', 'important');
  }
}

function checkRandomEvents() {
  // 豪强逼债事件
  if (gameState.humanWarmth >= 30 && !gameState.triggeredEvents.includes('debt_crisis')) {
    if (Math.random() < 0.3) {
      triggerEvent('debt_crisis');
      gameState.triggeredEvents.push('debt_crisis');
    }
  }

  // 年龄增长
  if (gameState.totalActions > 0 && gameState.totalActions % 20 === 0) {
    if (gameState.lampOil >= 1) {
      gameState.lampOil--;
      addLog('消耗1滴灯油延缓衰老。');
    } else {
      gameState.age++;
      addLog(`岁月流逝，顾迟年现年${gameState.age}岁。`);
    }
  }
}

function triggerEvent(eventId) {
  const event = STORY_EVENTS[eventId];
  if (!event) return;

  elements.eventTitle.textContent = event.title;
  elements.eventText.textContent = event.text;
  elements.eventChoices.innerHTML = '';

  event.choices.forEach((choice, index) => {
    const btn = document.createElement('button');
    btn.className = 'choice-btn';
    btn.innerHTML = choice.text;

    if (choice.cost) {
      const costText = [];
      if (choice.cost.lampOil) costText.push(`灯油-${choice.cost.lampOil}`);
      if (choice.cost.memories) costText.push(`记忆-${choice.cost.memories}`);
      btn.innerHTML += `<div class="choice-cost">消耗：${costText.join('、')}</div>`;
    }

    btn.onclick = () => {
      if (choice.cost && !applyCost(choice.cost)) {
        addLog('资源不足，无法选择此选项。');
        return;
      }
      applyReward(choice.effect);
      if (choice.log) {
        addLog(choice.log, 'event');
      }
      elements.eventModal.classList.add('hidden');
      updateUI();
      autoSave();
    };

    elements.eventChoices.appendChild(btn);
  });

  elements.eventModal.classList.remove('hidden');
}

function switchLocation(locationId) {
  const location = LOCATIONS[locationId];
  if (gameState.realm < location.unlockRealm) {
    addLog(`需要达到「${REALMS[location.unlockRealm].name}」阶才能前往${location.name.split('·')[0].trim()}`);
    return;
  }
  gameState.currentLocation = locationId;
  addLog(`前往${location.name}`);
  updateUI();
}

function updateNavButtons() {
  document.querySelectorAll('.nav-btn').forEach(btn => {
    const tab = btn.dataset.tab;
    const location = LOCATIONS[tab];
    btn.classList.toggle('active', tab === gameState.currentLocation);
    btn.disabled = gameState.realm < location.unlockRealm;
  });
}

// ========== 存档系统 ==========

function saveGame() {
  localStorage.setItem('elderCultivatorSave', JSON.stringify(gameState));
  addLog('存档成功。', 'important');
}

function loadGame() {
  const saved = localStorage.getItem('elderCultivatorSave');
  if (saved) {
    gameState = { ...gameState, ...JSON.parse(saved) };
    addLog('读取存档成功。', 'important');
    return true;
  }
  return false;
}

function autoSave() {
  localStorage.setItem('elderCultivatorSave', JSON.stringify(gameState));
}

function resetGame() {
  if (confirm('确定要重新开始吗？当前进度将丢失。')) {
    localStorage.removeItem('elderCultivatorSave');
    location.reload();
  }
}

// ========== 初始化 ==========

function init() {
  const hasSave = loadGame();

  if (!hasSave) {
    setTimeout(() => triggerEvent('prologue'), 500);
  }

  elements.cultivateBtn.onclick = cultivate;
  elements.convertBtn.onclick = convertWarmth;
  elements.saveBtn.onclick = saveGame;
  elements.resetBtn.onclick = resetGame;

  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.onclick = () => switchLocation(btn.dataset.tab);
  });

  elements.eventModal.onclick = (e) => {
    if (e.target === elements.eventModal) {
      elements.eventModal.classList.add('hidden');
    }
  };

  updateUI();
  addLog('游戏开始。愿你为人间留一盏永不熄灭的灯。');
}

document.addEventListener('DOMContentLoaded', init);
