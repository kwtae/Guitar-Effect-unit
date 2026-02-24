import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, Switch, TouchableOpacity, SafeAreaView, Dimensions } from 'react-native';

// Phase 9: AI Guitar Pedal - Mobile Native Controller (React Native / Expo)
// This code demonstrates the core logic for the Gig Mode interface and BLE/WiFi toggling.

const { width } = Dimensions.get('window');

export default function App() {
    const [isConnected, setIsConnected] = useState(false);
    const [connectionMode, setConnectionMode] = useState('WiFi'); // 'WiFi' or 'BLE'
    const [activePreset, setActivePreset] = useState("Clean Chorus");

    // Simulated hardware knobs
    const [gain, setGain] = useState(5.0);
    const [level, setLevel] = useState(7.5);

    useEffect(() => {
        // Simulated connection attempt to the Raspberry Pi FastAPI WebSocket or BLE Peripheral
        const connectToPedal = async () => {
            console.log(`Attempting to connect via ${connectionMode}...`);
            setTimeout(() => setIsConnected(true), 1500);
        };

        if (!isConnected) {
            connectToPedal();
        }
    }, [connectionMode, isConnected]);

    const sendParamChange = (param, value) => {
        // In production, this fires a WebSocket message: ws.send(JSON.stringify({param, value}))
        // Or a BLE characteristic write: bleManager.writeCharacteristic(...)
        console.log(`[${connectionMode} TX]: Changed ${param} to ${value}`);
    };

    const handleGainChange = (increment) => {
        const newVal = Math.max(0, Math.min(10, gain + increment));
        setGain(newVal);
        sendParamChange('gain', newVal);
    };

    return (
        <SafeAreaView style={styles.container}>
            {/* Header Panel */}
            <View style={styles.header}>
                <Text style={styles.title}>🎸 AI Pedal Stage Control</Text>
                <View style={styles.statusRow}>
                    <View style={[styles.statusDot, { backgroundColor: isConnected ? '#66fcf1' : '#ff4b4b' }]} />
                    <Text style={styles.statusText}>{isConnected ? `CONNECTED: ${connectionMode}` : 'SEARCHING...'}</Text>
                </View>

                {/* Connection Toggle (WiFi vs BLE for offline gig) */}
                <View style={styles.toggleRow}>
                    <Text style={styles.label}>Bluetooth (BLE) Gig Mode</Text>
                    <Switch
                        value={connectionMode === 'BLE'}
                        onValueChange={(val) => {
                            setIsConnected(false);
                            setConnectionMode(val ? 'BLE' : 'WiFi');
                        }}
                        trackColor={{ false: '#333', true: '#45a29e' }}
                        thumbColor={connectionMode === 'BLE' ? '#66fcf1' : '#f4f3f4'}
                    />
                </View>
            </View>

            {/* Gig Mode: Huge presets buttons for foot or quick thumb pressing on dark stage */}
            <View style={styles.gigModeSection}>
                <Text style={styles.sectionTitle}>STAGE PRESETS</Text>
                <TouchableOpacity
                    style={[styles.presetBtn, activePreset === "Clean Chorus" && styles.presetBtnActive]}
                    onPress={() => setActivePreset("Clean Chorus")}
                >
                    <Text style={styles.btnText}>Song 1: Clean Chorus</Text>
                </TouchableOpacity>

                <TouchableOpacity
                    style={[styles.presetBtn, activePreset === "Insane Fuzz" && styles.presetBtnActive]}
                    onPress={() => setActivePreset("Insane Fuzz")}
                >
                    <Text style={styles.btnText}>Song 2: Insane Fuzz</Text>
                </TouchableOpacity>
            </View>

            {/* Virtual Knobs (Live Tweaking) */}
            <View style={styles.knobSection}>
                <Text style={styles.sectionTitle}>LIVE TWEAK (DRIVE)</Text>
                <View style={styles.knobDisplay}>
                    <TouchableOpacity style={styles.knobBtn} onPress={() => handleGainChange(-0.5)}>
                        <Text style={styles.knobBtnText}>-</Text>
                    </TouchableOpacity>
                    <Text style={styles.knobValue}>{gain.toFixed(1)}</Text>
                    <TouchableOpacity style={styles.knobBtn} onPress={() => handleGainChange(0.5)}>
                        <Text style={styles.knobBtnText}>+</Text>
                    </TouchableOpacity>
                </View>
            </View>

            {/* RLHF Swipe Deck navigation hints */}
            <View style={styles.footer}>
                <TouchableOpacity style={styles.navBtn}>
                    <Text style={styles.navText}>Swipe AI Tutor >></Text>
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#0b0c10', paddingTop: 40 },
    header: { padding: 20, borderBottomWidth: 1, borderBottomColor: '#1f2833' },
    title: { fontSize: 24, fontWeight: '800', color: '#c5c6c7' },
    statusRow: { flexDirection: 'row', alignItems: 'center', marginTop: 10 },
    statusDot: { width: 10, height: 10, borderRadius: 5, marginRight: 8 },
    statusText: { color: '#c5c6c7', fontWeight: 'bold' },
    toggleRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 20, alignItems: 'center' },
    label: { color: '#45a29e', fontSize: 16 },
    gigModeSection: { padding: 20 },
    sectionTitle: { color: '#45a29e', fontSize: 14, fontWeight: 'bold', marginBottom: 15, letterSpacing: 1 },
    presetBtn: { backgroundColor: '#1f2833', padding: 20, borderRadius: 12, marginBottom: 15, alignItems: 'center' },
    presetBtnActive: { backgroundColor: 'rgba(102, 252, 241, 0.2)', borderColor: '#66fcf1', borderWidth: 1 },
    btnText: { color: '#fff', fontSize: 18, fontWeight: '600' },
    knobSection: { padding: 20, flex: 1 },
    knobDisplay: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#111', borderRadius: 20, padding: 10 },
    knobBtn: { width: 60, height: 60, backgroundColor: '#1f2833', borderRadius: 30, justifyContent: 'center', alignItems: 'center' },
    knobBtnText: { color: '#66fcf1', fontSize: 30, fontWeight: 'bold' },
    knobValue: { color: '#fff', fontSize: 40, fontWeight: '800', fontVariant: ['tabular-nums'] },
    footer: { padding: 20, paddingBottom: 40, borderTopWidth: 1, borderTopColor: '#1f2833' },
    navBtn: { alignItems: 'center', padding: 15, backgroundColor: 'rgba(255, 75, 75, 0.1)', borderRadius: 10 },
    navText: { color: '#ff4b4b', fontWeight: 'bold', fontSize: 16 }
});
