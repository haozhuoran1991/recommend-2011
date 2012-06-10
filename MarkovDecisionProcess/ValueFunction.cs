﻿﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Threading;
using System.Windows.Forms;

namespace MarkovDecisionProcess
{
    class ValueFunction : Policy
    {

        //more data structures here
        private Domain m_dDomain;
        public double MaxValue { get; private set; }
        public double MinValue { get; private set; }

        private Dictionary<State, double> ViByS;
        private Dictionary<State, double> Vi_1ByS;
        private Dictionary<State, Action> ViBySActions;
        private Dictionary<State ,Dictionary<Action, double>> Q;

        public ValueFunction(Domain d)
        {
            //your code here
            m_dDomain = d;
            MaxValue = 0.0;
            MinValue = 0.0;

            ViByS = new Dictionary<State, double>();
            Vi_1ByS = new Dictionary<State, double>();
            ViBySActions = new Dictionary<State, Action>();

            Q = new Dictionary<State, Dictionary<Action, double>>();
        }

        // init all V0(s) to 0
        private void initV0()
        {
            foreach (State s in m_dDomain.States)
            {
                ViByS.Add(s, 0.0);
                Vi_1ByS.Add(s, 0);
                ViBySActions.Add(s, null);
            }
        }

        public double ValueAt(State s)
        {
            //your code here
            return Vi_1ByS[s];
        }

        public override Action GetAction(State s)
        {
            //your code here
            return ViBySActions[s];
        }

        public void ValueIteration(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting value iteration");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;

            //your code here
            initV0();
            double delta, maxDelta;
            do
            {
                maxDelta = Double.MinValue;
                foreach (State s in m_dDomain.States)
                {
                    delta = updateValueIter(s);
                    cUpdates++;
                    maxDelta = Math.Max(delta, maxDelta);
                }
                Console.WriteLine(maxDelta);
                ViByS = new Dictionary<State, double>(Vi_1ByS);
            } while (maxDelta >= dEpsilon);

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished value iteration");
        }

        // calc the formula for Vi+1(s)
        private double updateValueIter(State s)
        {
            double maxV = Double.MinValue;
            Action maxA = null;
            foreach (Action a in m_dDomain.Actions)
            {
                // clac formula for action a
                double sum = 0;
                foreach (State stag in s.Successors(a))
                    sum += s.TransitionProbability(a, stag) * ViByS[stag];
                double tmp = s.Reward(a) + m_dDomain.DiscountFactor * sum;
                // save max
                if((tmp >= maxV) && (!s.Apply(a).Equals(s))){
                    maxV = tmp;
                    maxA = a;
                }
            }
            if (maxA != null)
            {
                Vi_1ByS[s] = maxV;
                ViBySActions[s] = maxA;
                return Math.Abs(maxV - ViByS[s]);
            }
            return 0;
        }

        public void LearningQ(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting learning-q");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;
            Application.DoEvents();
            
            //your code here
            initV0();
            foreach(State s in m_dDomain.States){
                Dictionary<Action , double> d = new Dictionary<Action,double>();
                foreach (Action a in m_dDomain.Actions)
                    d.Add(a, 0);
                Q.Add(s, d);
            }

            State i = m_dDomain.StartState , j;
            Action chosenA = null;
            do
            {
                chosenA = findMaxQA(i);
                j = i.Apply(chosenA);
                double r = i.Reward(chosenA);
                Q[i][chosenA] = dEpsilon*Q[i][chosenA] + (1 - dEpsilon)*(r + m_dDomain.DiscountFactor *Q[j][findMaxQA(j)]);
                i = j;
            } while (!m_dDomain.IsGoalState(i));
            
            setActions();

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished learning-q");
        }

        private void setActions()
        {
            foreach (State s in m_dDomain.States)
                ViBySActions.Add(s, findMaxQA(s));
        }

        private Action findMaxQA(State j)
        {
            List<Action> actions = new List<Action>();
            double maxQA = double.MinValue;
            foreach (Action a in m_dDomain.Actions)
            {
                if (Q[j][a] > maxQA)
                    maxQA = Q[j][a];
                if (Q[j][a] == maxQA)
                    actions.Add(a);
            }
            int idx = RandomGenerator.Next(actions.Count);
            return actions[idx];
        }

        public void Sarsa(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting SARSA");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;
            Application.DoEvents();
            
            //your code here
            initV0();
            RandomPolicy rn = new RandomPolicy(m_dDomain);
            foreach (State s in m_dDomain.States)
                ViBySActions[s] = rn.GetAction(s);
            State i = m_dDomain.StartState, j;
            Action chosenA = null;
            do
            {
                chosenA = GetAction(i);
                j = i.Apply(chosenA);
                double r = i.Reward(chosenA);
                ViByS[i] = dEpsilon * ViByS[i] + (1 - dEpsilon) * (r +  ViByS[j]);
                i = j;
            } while (!m_dDomain.IsGoalState(i));
            
            setActions();

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished SARSA");
        }

    }
}