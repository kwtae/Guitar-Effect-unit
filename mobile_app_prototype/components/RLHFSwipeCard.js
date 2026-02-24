import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Animated, PanResponder, Dimensions } from 'react-native';

const { width } = Dimensions.get('window');

// Phase 9: AI Guitar Pedal - RLHF Swipe UI Component
// This is the "Tinder-like" evaluating screen where users practice their instrument,
// hear the AI's parameter generation, and quickly swipe Right (Keep) or Left (Reject & Recalculate).

export default function RLHFSwipeCard({ targetTone = "Marshall JCM800 Metal Fuzz", generatedParams }) {
    const [swipeAnim] = useState(new Animated.ValueXY());

    const panResponder = PanResponder.create({
        onStartShouldSetPanResponder: () => true,
        onPanResponderMove: Animated.event([null, { dx: swipeAnim.x, dy: swipeAnim.y }], { useNativeDriver: false }),
        onPanResponderRelease: (e, gesture) => {
            if (gesture.dx > 120) {
                // Swiped Right -> Accept Tone
                Animated.spring(swipeAnim, { toValue: { x: width + 100, y: gesture.dy }, useNativeDriver: false }).start(() => {
                    console.log("🟢 RLHF: User ACCEPTED AI Tone.");
                    // In Production: Axios.post('/rlhf-feedback/', { status: 'accepted' })
                });
            } else if (gesture.dx < -120) {
                // Swiped Left -> Reject Tone
                Animated.spring(swipeAnim, { toValue: { x: -width - 100, y: gesture.dy }, useNativeDriver: false }).start(() => {
                    console.log("🔴 RLHF: User REJECTED AI Tone. Sending back to Gemini for recalibration...");
                    // In Production: Axios.post('/rlhf-feedback/', { status: 'rejected' })
                });
            } else {
                // Reset if didn't swipe far enough
                Animated.spring(swipeAnim, { toValue: { x: 0, y: 0 }, friction: 4, useNativeDriver: false }).start();
            }
        }
    });

    const cardStyle = {
        transform: swipeAnim.getTranslateTransform(),
    };

    return (
        <View style={styles.container}>
            <Text style={styles.topText}>Does this sound accurate?</Text>
            <Animated.View style={[styles.card, cardStyle]} {...panResponder.panHandlers}>
                <Text style={styles.title}>AI Generation Result</Text>
                <Text style={styles.subtitle}>Target: {targetTone}</Text>

                <View style={styles.paramBox}>
                    <Text style={styles.paramText}>🎸 Drive: 7.5</Text>
                    <Text style={styles.paramText}>🎛️ Tone: 4.2</Text>
                    <Text style={styles.paramText}>🔊 Level: 8.0</Text>
                </View>

                <View style={styles.instructionRow}>
                    <Text style={styles.redText}>&lt;&lt; REJECT (Too Muddy)</Text>
                    <Text style={styles.greenText}>PERFECT &gt;&gt;</Text>
                </View>
            </Animated.View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#0b0c10', justifyContent: 'center', alignItems: 'center' },
    topText: { color: '#c5c6c7', fontSize: 18, marginBottom: 20 },
    card: {
        width: width * 0.85,
        height: 400,
        backgroundColor: 'rgba(31, 40, 51, 0.9)',
        borderRadius: 20,
        padding: 20,
        justifyContent: 'center',
        borderWidth: 1,
        borderColor: 'rgba(102, 252, 241, 0.3)',
        shadowColor: '#66fcf1',
        shadowOffset: { width: 0, height: 10 },
        shadowOpacity: 0.1,
        shadowRadius: 20,
    },
    title: { color: '#66fcf1', fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginBottom: 10 },
    subtitle: { color: '#ffffff', fontSize: 16, textAlign: 'center', marginBottom: 30 },
    paramBox: { backgroundColor: '#111', padding: 20, borderRadius: 10, marginBottom: 30 },
    paramText: { color: '#c5c6c7', fontSize: 18, marginVertical: 5, fontWeight: 'bold' },
    instructionRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 'auto' },
    redText: { color: '#ff4b4b', fontWeight: 'bold' },
    greenText: { color: '#66fcf1', fontWeight: 'bold' }
});
