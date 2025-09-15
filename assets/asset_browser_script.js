// Asset Browser JavaScript
class AssetBrowser {
    constructor() {
        this.currentCategory = 'scripts';
        this.assets = this.initializeAssets();
        this.filteredAssets = [];
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.renderAssets();
        this.setupCategorySelection();
    }
    
    initializeAssets() {
        return {
            scripts: [
                { name: 'PlayerController.cs', icon: 'code', type: 'script' },
                { name: 'GameManager.cs', icon: 'code', type: 'script' },
                { name: 'UIController.cs', icon: 'code', type: 'script' },
                { name: 'AudioManager.cs', icon: 'code', type: 'script' }
            ],
            textures: [
                { name: 'player_diffuse.png', icon: 'image', type: 'texture' },
                { name: 'ground_texture.jpg', icon: 'image', type: 'texture' },
                { name: 'ui_background.png', icon: 'image', type: 'texture' },
                { name: 'particle_glow.png', icon: 'image', type: 'texture' }
            ],
            audio: [
                { name: 'background_music.mp3', icon: 'audio', type: 'audio' },
                { name: 'jump_sound.wav', icon: 'audio', type: 'audio' },
                { name: 'collect_item.wav', icon: 'audio', type: 'audio' },
                { name: 'menu_click.wav', icon: 'audio', type: 'audio' }
            ],
            models: [
                { name: 'player_model.fbx', icon: 'model', type: 'model' },
                { name: 'environment_props.fbx', icon: 'model', type: 'model' },
                { name: 'weapon_sword.obj', icon: 'model', type: 'model' },
                { name: 'building_house.fbx', icon: 'model', type: 'model' }
            ],
            prefabs: [
                { name: 'Player.prefab', icon: 'prefab', type: 'prefab' },
                { name: 'Enemy.prefab', icon: 'prefab', type: 'prefab' },
                { name: 'Collectible.prefab', icon: 'prefab', type: 'prefab' },
                { name: 'UI_Panel.prefab', icon: 'prefab', type: 'prefab' }
            ]
        };
    }
    
    setupEventListeners() {
        // Search functionality
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filterAssets(e.target.value);
            });
        }
        
        // Import button
        const importButton = document.querySelector('.import-button');
        if (importButton) {
            importButton.addEventListener('click', () => {
                this.importAsset();
            });
        }
    }
    
    setupCategorySelection() {
        const categories = document.querySelectorAll('.asset-category');
        categories.forEach(category => {
            category.addEventListener('click', () => {
                const categoryName = category.dataset.category;
                this.selectCategory(categoryName);
            });
        });
    }
    
    selectCategory(categoryName) {
        this.currentCategory = categoryName;
        this.updateCategoryUI(categoryName);
        this.renderAssets();
        
        // Notify Python bridge
        if (window.pythonBridge && window.pythonBridge.categoryChanged) {
            window.pythonBridge.categoryChanged(categoryName);
        }
    }
    
    updateCategoryUI(selectedCategory) {
        const categories = document.querySelectorAll('.asset-category');
        categories.forEach(category => {
            if (category.dataset.category === selectedCategory) {
                category.style.background = 'linear-gradient(90deg, rgba(255, 140, 66, 0.2) 0%, rgba(255, 140, 66, 0.1) 100%)';
                category.style.border = '1px solid rgba(255, 140, 66, 0.3)';
            } else {
                category.style.background = 'transparent';
                category.style.border = 'none';
            }
        });
    }
    
    filterAssets(searchTerm) {
        if (!searchTerm.trim()) {
            this.filteredAssets = this.assets[this.currentCategory] || [];
        } else {
            const allAssets = Object.values(this.assets).flat();
            this.filteredAssets = allAssets.filter(asset => 
                asset.name.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }
        this.renderAssets();
    }
    
    renderAssets() {
        const assetGrid = document.getElementById('assetGrid');
        if (!assetGrid) return;
        
        const assetsToRender = this.filteredAssets.length > 0 ? this.filteredAssets : (this.assets[this.currentCategory] || []);
        
        assetGrid.innerHTML = assetsToRender.map((asset, index) => {
            const delay = index * 30;
            return `
                <div class="asset-item" 
                     style="animation-delay: ${delay}ms;"
                     data-asset-name="${asset.name}"
                     data-asset-type="${asset.type}">
                    <div class="asset-icon">
                        ${this.getAssetIcon(asset.icon)}
                    </div>
                    <span class="asset-name" title="${asset.name}">${asset.name}</span>
                </div>
            `;
        }).join('');
        
        this.setupAssetClickHandlers();
    }
    
    getAssetIcon(iconType) {
        const icons = {
            code: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M16 18l6-6-6-6M8 6l-6 6 6 6" stroke="currentColor" stroke-width="2" fill="none"></path>
            </svg>`,
            image: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2" fill="none"></rect>
                <circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"></circle>
                <path d="M21 15l-5-5L5 21" stroke="currentColor" stroke-width="2" fill="none"></path>
            </svg>`,
            audio: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M9 18V5l12-2v13" stroke="currentColor" stroke-width="2" fill="none"></path>
                <circle cx="6" cy="18" r="3" stroke="currentColor" stroke-width="2" fill="none"></circle>
                <circle cx="18" cy="16" r="3" stroke="currentColor" stroke-width="2" fill="none"></circle>
            </svg>`,
            model: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <rect x="2" y="3" width="20" height="5" rx="1" stroke="currentColor" stroke-width="2" fill="none"></rect>
                <path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8M10 12h4" stroke="currentColor" stroke-width="2"></path>
            </svg>`,
            prefab: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M12 2l8 4v12l-8 4-8-4V6l8-4z" stroke="currentColor" stroke-width="2" fill="none"></path>
                <path d="M12 6v12M4 6l8 6 8-6" stroke="currentColor" stroke-width="2"></path>
            </svg>`
        };
        
        return icons[iconType] || icons.code;
    }
    
    setupAssetClickHandlers() {
        const assetItems = document.querySelectorAll('.asset-item');
        assetItems.forEach(item => {
            item.addEventListener('click', () => {
                const assetName = item.dataset.assetName;
                const assetType = item.dataset.assetType;
                this.selectAsset(assetName, assetType);
            });
        });
    }
    
    selectAsset(assetName, assetType) {
        // Notify Python bridge
        if (window.pythonBridge && window.pythonBridge.assetSelected) {
            window.pythonBridge.assetSelected(assetName, assetType);
        }
        
        // Visual feedback
        const allAssets = document.querySelectorAll('.asset-item');
        allAssets.forEach(asset => {
            asset.style.border = '1px solid rgba(255, 255, 255, 0.1)';
        });
        
        const selectedAsset = document.querySelector(`[data-asset-name="${assetName}"]`);
        if (selectedAsset) {
            selectedAsset.style.border = '2px solid #ff8c42';
            selectedAsset.style.boxShadow = '0 0 20px rgba(255, 140, 66, 0.3)';
        }
    }
    
    importAsset() {
        // Notify Python bridge
        if (window.pythonBridge && window.pythonBridge.importAsset) {
            window.pythonBridge.importAsset();
        }
        
        // Show import dialog (placeholder)
        console.log('Import asset functionality triggered');
    }
    
    // Public API methods
    setCategory(categoryName) {
        if (this.assets[categoryName]) {
            this.selectCategory(categoryName);
        }
    }
    
    addAsset(category, asset) {
        if (!this.assets[category]) {
            this.assets[category] = [];
        }
        this.assets[category].push(asset);
        this.renderAssets();
    }
    
    removeAsset(category, assetName) {
        if (this.assets[category]) {
            this.assets[category] = this.assets[category].filter(asset => asset.name !== assetName);
            this.renderAssets();
        }
    }
    
    refreshAssets() {
        this.renderAssets();
    }
}

// Initialize asset browser when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.assetBrowser = new AssetBrowser();
    
    // Setup Python bridge
    window.pythonBridge = {
        categoryChanged: function(category) {
            console.log('Category changed to:', category);
        },
        assetSelected: function(assetName, assetType) {
            console.log('Asset selected:', assetName, 'Type:', assetType);
        },
        importAsset: function() {
            console.log('Import asset requested');
        }
    };
    
    console.log('Asset Browser initialized successfully');
});

// Prevent zooming
document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && 
        (e.key === '+' || e.key === '-' || e.key === '=' || e.key === '0')) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }
}, true);

document.addEventListener('wheel', function(e) {
    if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }
}, { passive: false });
