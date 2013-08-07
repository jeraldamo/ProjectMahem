# -*- coding: utf-8 -*-
"""
testsuite.py
A unit-testing environment for python
"""

from imports import *

  
import os
import inspect


class TestSuite():
    curTestCount = 0
    tests = []

    @staticmethod
    def addAssertion(assertion):
        TestSuite.tests[TestSuite.curTestCount][1].append(assertion)

def test(func):
    if not __debug__:
        def debug_off():
            print "Test function [%s] is nullified as __debug__ is False" %func.__name__        
        return None
    
    #print func.__module__
    if func.__module__ == '__main__':
        filename = getCallerInfo().filename
        if '.pyc' in filename:
            filename = filename[:4]
        elif '.py' in filename:
            filename = filename[:-3]
    else:
        filename = func.__module__
    TestSuite.tests.append([func.__name__, [], True, filename])
    func()
    TestSuite.curTestCount += 1



def reportTests(log=None):
    redColor = '\033[91m'
    greenColor = '\033[92m'
    yellowColor = '\033[93m'
    blueColor = '\033[94m'
    endColor = '\033[0m'
    if log:
        log = open(log, 'w')
    os.system('clear')
    for testIndex, test in enumerate(TestSuite.tests, start=1):
        print 'Test %s: %s%s%s in %s' %(testIndex, blueColor, test[0], endColor, test[3])
        
        if log:
            log.write('Test %s: %s in %s\n' %(testIndex, test[0], test[3]))
            
        for assertionIndex, assertion in enumerate(test[1], start=1):
            if assertion['pass']:
                print '... [Assertion %s] %sPASS%s' %(assertionIndex, greenColor, endColor)
                if log:
                    log.write('... [Assertion %s] PASS\n' %assertionIndex)
            else:
                print '... [Assertion %s] %sFAIL%s' %(assertionIndex, redColor, endColor)
                if log:
                    log.write('... [Assertion %s] FAIL\n' %assertionIndex)
                test[2] = False
                
            print '... ... [Assertion Type]', assertion['test'], 'line:', assertion['callerInfo'].lineno
            print '... ... [Conditions]    ', assertion['conditions']
            print '... ... [Exception]     ', assertion['exception']
            print
            
            if log:
                log.write('... ... [Assertion Type] %s line: %s\n' %(assertion['test'], assertion['callerInfo'].lineno))
                log.write('... ... [Conditions]     %s\n' %str(assertion['conditions']))
                log.write('... ... [Exception]      %s\n' %assertion['exception'])
                log.write('\n')
        print
        if log:
            log.write('\n')
            
    passCount = 0
    failCount = 0
    
    for testIndex, test in enumerate(TestSuite.tests, start=1):
        if test[2]:
            print 'Test %s [%s] %sPassed%s' %(testIndex, test[0], greenColor, endColor)
            if log:
                log.write('Test %s [%s] Passed\n' %(testIndex, test[0]))
            passCount += 1
        else:
            print 'Test %s [%s] %sFailed%s' %(testIndex, test[0], redColor, endColor)
            if log:
                log.write('Test %s [%s] Failed\n' %(testIndex, test[0]))
            failCount += 1
    
    print
    if failCount == 0:
        print "%sTestsuite Passed (%s test(s) passed, %s test(s) failed)%s" %(greenColor, passCount, failCount, endColor)
        if log:
            log.write("Testsuite Passed (%s test(s) passed, %s test(s) failed)\n" %(passCount, failCount))
        
    else:
        print "%sTestSuite Failed (%s test(s) passed, %s test(s) failed)%s" %(redColor, passCount, failCount, endColor)
        if log:
            log.write("TestSuite Failed (%s test(s) passed, %s test(s) failed)\n" %(passCount, failCount))

    return failCount

def getCallerInfo():
    return inspect.getframeinfo(inspect.stack()[2][0])
        
def assertTrue(conditionA):
    try:
        assertion = {'test': 'assertTrue', 'conditions': (conditionA), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA:
            assertion['pass'] = True
        else:
            assertion['pass'] = False
    
    except Exception, e:
        assertion['exception'] = e
    
    TestSuite.addAssertion(assertion)
        
def assertFalse(conditionA):
    try:
        assertion = {'test': 'assertFalse', 'conditions': (conditionA), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA:
            assertion['pass'] = False
        else:
            assertion['pass'] = True
    
    except Exception, e:
        assertion['exception'] = e
            
    TestSuite.addAssertion(assertion)
    
def assertEqual(conditionA, conditionB):
    try:
        assertion = {'test': 'assertEquals', 'conditions': (conditionA, conditionB), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA == conditionB:
            assertion['pass'] = True
        else:
            assertion['pass'] = False
    
    except Exception, e:
        assertion['exception'] = e
            
    TestSuite.addAssertion(assertion)
    
def assertNotEqual(conditionA, conditionB):
    try:
        assertion = {'test': 'assertNotEquals', 'conditions': (conditionA, conditionB), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA == conditionB:
            assertion['pass'] = False
        else:
            assertion['pass'] = True
    
    except Exception, e:
        assertion['exception'] = e
            
    TestSuite.addAssertion(assertion)
    
def assertEqualReference(conditionA, conditionB):
    try:
        assertion = {'test': 'assertEqualReference', 'conditions': (conditionA, conditionB), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA is conditionB:
            assertion['pass'] = True
        else:
            assertion['pass'] = False
    
    except Exception, e:
        assertion['exception'] = e
            
    TestSuite.addAssertion(assertion)

def assertNotEqualReference(conditionA, conditionB):
    try:
        assertion = {'test': 'assertNotEqualReference', 'conditions': (conditionA, conditionB), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA is conditionB:
            assertion['pass'] = False
        else:
            assertion['pass'] = True
    
    except Exception, e:
        assertion['exception'] = e
            
    TestSuite.addAssertion(assertion)
    
def assertGreaterThan(conditionA, conditionB):
    try:
        assertion = {'test': 'assertGreaterThan', 'conditions': (conditionA, conditionB), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA > conditionB:
            assertion['pass'] = True
        else:
            assertion['pass'] = False
    
    except Exception, e:
        assertion['exception'] = e
            
    TestSuite.addAssertion(assertion)
    
def assertGreaterThanEqualTo(conditionA, conditionB):
    try:
        assertion = {'test': 'assertGreaterThanEqualTo', 'conditions': (conditionA, conditionB), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA >= conditionB:
            assertion['pass'] = True
        else:
            assertion['pass'] = False
    
    except Exception, e:
        assertion['exception'] = e
            
    TestSuite.addAssertion(assertion)
    
def assertLessThan(conditionA, conditionB):
    try:
        assertion = {'test': 'assertLessThan', 'conditions': (conditionA, conditionB), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA < conditionB:
            assertion['pass'] = True
        else:
            assertion['pass'] = False
    
    except Exception, e:
        assertion['exception'] = e
            
    TestSuite.addAssertion(assertion)    
    
def assertLessThanEqualTo(conditionA, conditionB):
    try:
        assertion = {'test': 'assertLessThanEqualTo', 'conditions': (conditionA, conditionB), 'exception': None, 'callerInfo': getCallerInfo()}
        if conditionA <= conditionB:
            assertion['pass'] = True
        else:
            assertion['pass'] = False
    
    except Exception, e:
        assertion['exception'] = e
            
    TestSuite.addAssertion(assertion)
